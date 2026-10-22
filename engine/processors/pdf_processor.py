"""PDF processor: HTML+CSS → single-page PDF via Playwright."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from engine.processors.base import FormatProcessor
from engine.utils.html import ensure_full_document, extract_html_from_llm
from engine.utils.screenshot import html_to_pdf, is_available as playwright_available

logger = logging.getLogger(__name__)


class PdfProcessor(FormatProcessor):
    """Render HTML to A4 PDF.

    Falls back to saving HTML source if Playwright is unavailable.
    """

    def process(self, content, doc_id, output_dir, template_path=None, metadata=None):
        self._ensure_dir(output_dir)

        doc_name = (metadata or {}).get("doc_name", doc_id)
        slug = doc_id.lower()
        name_slug = self._slugify(doc_name)
        base_name = f"{slug}_{name_slug}_render"

        if isinstance(content, dict) and template_path:
            from engine.utils.html import load_and_inject
            html = load_and_inject(Path(template_path), content)
        elif isinstance(content, str):
            html = extract_html_from_llm(content)
        else:
            html = str(content)
        html = ensure_full_document(html)
        html = self._inject_print_css(html)

        html_path = output_dir / f"{base_name}.html"
        html_path.write_text(html, encoding="utf-8")
        logger.info(f"PdfProcessor [{doc_id}]: saved intermediate HTML → {html_path}")

        pdf_path = output_dir / f"{base_name}.pdf"

        if playwright_available():
            success = html_to_pdf(
                html,
                pdf_path,
                format="A4",
                print_background=True,
                margin={
                    "top": "15mm",
                    "right": "15mm",
                    "bottom": "15mm",
                    "left": "15mm",
                },
            )
            if success:
                return pdf_path

        logger.warning(
            f"PdfProcessor [{doc_id}]: Playwright unavailable. Use {html_path} instead."
        )
        return html_path

    @staticmethod
    def _inject_print_css(html: str) -> str:
        """Add print-optimized CSS before </head>."""
        print_css = """
<style>
  @media print {
    body { font-size: 11pt; line-height: 1.5; }
    .container { max-width: 100%; width: 100%; }
    h1 { page-break-before: always; }
    h1:first-of-type { page-break-before: avoid; }
    table, .no-break { page-break-inside: avoid; }
  }
  @page { size: A4; margin: 15mm; }
</style>"""
        if "</head>" in html:
            return html.replace("</head>", f"{print_css}\n</head>")
        return f"{print_css}\n{html}"

    @staticmethod
    def _strip_fences(text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("```"):
            lines = stripped.split("\n")
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            return "\n".join(lines).strip()
        return stripped