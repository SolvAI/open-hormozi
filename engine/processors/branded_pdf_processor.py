"""Branded PDF processor: LLM HTML + brand CSS → editorial PDF.

The LLM outputs an HTML fragment using the classes defined in templates/brand/.
This processor wraps it in a full document — navy cover sheet, running header,
footer with page numbers — and renders it to A4.

Pipeline:  LLM HTML body ──► cover doc + body doc (variables.css + style.css)
           Playwright pdf() ──► cover.pdf (full bleed) + body.pdf (header/footer)
           pypdf merge ───────► final A4 PDF
           (fallback) ────────► single-pass PDF, else .html file

Why two renders: Chromium ignores CSS `@page` margin boxes, so page numbers have
to come from Playwright's header/footer templates — and those paint on *every*
page, including over the cover. Rendering the cover separately (zero margins, no
templates) and merging is the only way to get both a full-bleed cover and
automatic page numbers in one document. If pypdf is unavailable the processor
falls back to a single pass, which still produces a valid PDF — just with the
running header/footer printed over the cover.
"""

from __future__ import annotations

import logging
import tempfile
from datetime import datetime
from html import escape as _esc
from pathlib import Path
from typing import Any
import base64

from engine.processors.base import FormatProcessor
from engine.utils.html import validate_html
from engine.utils.screenshot import html_to_pdf, is_available as playwright_available

logger = logging.getLogger(__name__)

_BRAND_DIR = Path("templates/brand")

_BRAND_NAME = "OpenHormozi"
_BRAND_URL = "github.com/SolvAI/open-hormozi"

# A4 print margins. The cover bleeds past these via a negative margin, so the
# two must stay in sync with `.cover` in style.css.
_MARGIN = {"top": "18mm", "right": "16mm", "bottom": "18mm", "left": "16mm"}


# Screen-only shell for the .html companion file. Never used for the PDF.
_PREVIEW_CSS = """
body {
  background: #e8e8ed;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 24px;
  min-height: 100vh;
}
.cover, .page {
  width: 100%;
  max-width: 172mm;
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 8px 24px rgba(0,0,0,.04);
}
.cover {
  margin: 0 0 32px 0;
  min-height: 240mm;
}
.page {
  background: #fff;
  padding: 34px 38px;
  border-radius: 2px;
}
@media print {
  body { background: white; padding: 0; display: block; }
  .cover, .page { box-shadow: none; max-width: 100%; }
  .page { padding: 0; border-radius: 0; }
}
"""

# Cover pass: the page itself carries zero margins so the navy bleeds to the
# paper edge. `.cover` supplies its own inset.
_COVER_ONLY_CSS = """
@page { size: A4; margin: 0; }
body { margin: 0; }
.cover { break-after: auto; page-break-after: auto; }
"""


_MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


def _display_date(when: datetime) -> str:
    """`August 12, 2026`, independent of the system locale."""
    return f"{_MONTHS[when.month - 1]} {when.day}, {when.year}"


class BrandedPdfProcessor(FormatProcessor):

    def process(
        self,
        content: Any,
        doc_id: str,
        output_dir: Path,
        template_path: str | None = None,
        metadata: dict | None = None,
    ) -> Path:
        self._ensure_dir(output_dir)
        meta = metadata or {}
        doc_name = meta.get("doc_name", doc_id)
        client_label = meta.get("client_label", "")

        body_html = content if isinstance(content, str) else str(content)
        body_html = self._strip_fences(body_html)

        embedded_html = self._embed_visuals(meta.get("visual_assets", {}))

        issues = validate_html(body_html)
        if issues:
            logger.info(f"BrandedPdfProcessor [{doc_id}]: {issues}")

        cover_html = self._build_cover(doc_id, doc_name, client_label)
        page_html = f'<div class="page">\n  {embedded_html}\n\n  {body_html}\n</div>'

        slug = f"{doc_id}_{self._slugify(doc_name)}"

        # Browser-readable version — cover and body in one scrollable document
        html_path = output_dir / f"{slug}.html"
        html_path.write_text(
            self._document(cover_html + "\n" + page_html, _PREVIEW_CSS, doc_id, doc_name),
            encoding="utf-8",
        )

        pdf_path = output_dir / f"{slug}.pdf"
        if playwright_available():
            if self._render_pdf(cover_html, page_html, pdf_path, doc_id, doc_name):
                logger.info(f"BrandedPdfProcessor: wrote {pdf_path}")
                return pdf_path
            logger.warning(f"BrandedPdfProcessor [{doc_id}]: PDF render failed")

        logger.warning(
            f"BrandedPdfProcessor [{doc_id}]: falling back to {html_path}"
        )
        return html_path

    # ─── Rendering ───────────────────────────────────────────

    def _render_pdf(
        self,
        cover_html: str,
        page_html: str,
        pdf_path: Path,
        doc_id: str,
        doc_name: str,
    ) -> bool:
        """Render cover and body separately, then merge.

        Falls back to a single pass when pypdf is missing.
        """
        header = self._header_template(doc_id, doc_name)
        footer = self._footer_template()

        try:
            from pypdf import PdfWriter
        except ImportError:
            logger.info(
                "pypdf not installed — rendering in one pass "
                "(running header/footer will print over the cover)"
            )
            return html_to_pdf(
                self._document(cover_html + "\n" + page_html, "", doc_id, doc_name),
                pdf_path,
                format="A4",
                print_background=True,
                margin=_MARGIN,
                header_template=header,
                footer_template=footer,
            )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            cover_pdf = tmp_dir / "cover.pdf"
            body_pdf = tmp_dir / "body.pdf"

            # Cover: full bleed, no running header/footer
            cover_ok = html_to_pdf(
                self._document(cover_html, _COVER_ONLY_CSS, doc_id, doc_name),
                cover_pdf,
                format="A4",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )

            # Body: normal margins, page numbers
            body_ok = html_to_pdf(
                self._document(page_html, "", doc_id, doc_name),
                body_pdf,
                format="A4",
                print_background=True,
                margin=_MARGIN,
                header_template=header,
                footer_template=footer,
            )

            if not body_ok:
                return False
            if not cover_ok:
                # Body alone is still a usable deliverable
                body_pdf.replace(pdf_path)
                return True

            writer = PdfWriter()
            writer.append(str(cover_pdf))
            writer.append(str(body_pdf))
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            with pdf_path.open("wb") as fh:
                writer.write(fh)
            writer.close()

        return True

    # ─── Running header / footer (Playwright templates) ──────

    def _header_template(self, doc_id: str, doc_name: str) -> str:
        """Chromium hides the header on page 1 only if we do it ourselves —
        it has no first-page selector, so the cover simply overlaps it with
        its own background."""
        label = _esc(f"{_BRAND_NAME} · {doc_id} · {doc_name}")
        return (
            '<div style="width:100%;font-family:-apple-system,Segoe UI,Helvetica,'
            'Arial,sans-serif;font-size:7pt;color:#7b828e;letter-spacing:.04em;'
            'padding:0 16mm;margin-top:8mm;">'
            '<div style="border-bottom:1px solid #e6e9ef;padding-bottom:4px;'
            f'display:flex;justify-content:space-between;"><span>{label}</span>'
            '<span></span></div></div>'
        )

    def _footer_template(self) -> str:
        return (
            '<div style="width:100%;font-family:-apple-system,Segoe UI,Helvetica,'
            'Arial,sans-serif;font-size:7pt;color:#7b828e;letter-spacing:.04em;'
            'padding:0 16mm;margin-bottom:8mm;">'
            '<div style="border-top:1px solid #e6e9ef;padding-top:4px;'
            'display:flex;justify-content:space-between;">'
            f'<span>{_BRAND_URL}</span>'
            '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span>'
            '</div></div>'
        )

    # ─── Cover ───────────────────────────────────────────────

    def _build_cover(self, doc_id: str, doc_name: str, client_label: str) -> str:
        client_line = (
            f'<div class="cover-client">{_esc(client_label)}</div>'
            if client_label else ""
        )
        return f"""<div class="cover">
  <div class="cover-brand">{_BRAND_NAME}</div>
  <div class="cover-body">
    <div class="cover-docid">{_esc(doc_id)}</div>
    <div class="cover-title">{_esc(doc_name)}</div>
    <div class="cover-divider"></div>
    {client_line}
    <div class="cover-meta">Growth strategy · {_display_date(datetime.now())}</div>
  </div>
  <div class="cover-footer">
    <span>{_BRAND_URL}</span>
    <span>Confidential</span>
  </div>
</div>"""

    # ─── Visual embedding ────────────────────────────────────

    def _embed_visuals(self, visual_assets: dict) -> str:
        """Base64-encode visual PNGs for inline embedding in the PDF."""
        if not visual_assets:
            return ""

        parts = []
        for fmt, path in visual_assets.items():
            if not isinstance(path, Path) or not path.exists():
                continue
            if path.suffix != ".png":
                continue
            try:
                b64 = base64.b64encode(path.read_bytes()).decode("ascii")
                label = path.stem.replace("_", " ").capitalize()
                parts.append(
                    '<figure class="figure">'
                    f'<img src="data:image/png;base64,{b64}" alt="{_esc(label)}">'
                    f"<figcaption>{_esc(label)}</figcaption>"
                    "</figure>"
                )
            except Exception as e:
                logger.warning(f"Failed to embed {path}: {e}")

        return "\n".join(parts)

    # ─── Document assembly ───────────────────────────────────

    def _document(self, inner: str, extra_css: str, doc_id: str, doc_name: str) -> str:
        """Wrap content in a full HTML document carrying the brand stylesheets."""
        variables_css = self._read_brand("variables.css")
        style_css = self._read_brand("style.css")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(doc_id)} — {_esc(doc_name)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700\
&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600\
&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{variables_css}
{style_css}
{extra_css}
</style>
</head>
<body>

{inner}

</body>
</html>"""

    # ─── Helpers ──────────────────────────────────────────────

    @staticmethod
    def _read_brand(filename: str) -> str:
        path = _BRAND_DIR / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        logger.warning(f"Brand file missing: {path}")
        return ""

    @staticmethod
    def _strip_fences(text: str) -> str:
        """Remove ```html ... ``` wrapping if LLM added it."""
        stripped = text.strip()
        if stripped.startswith("```"):
            lines = stripped.split("\n")
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            return "\n".join(lines).strip()
        return stripped
