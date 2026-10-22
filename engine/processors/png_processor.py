"""PNG processor: HTML+CSS → screenshot PNG.

Two modes:
  1. LLM_THEN_RENDER: LLM returns JSON → inject into HTML template → screenshot
  2. Direct: LLM returns full HTML+CSS → screenshot as-is
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from engine.processors.base import FormatProcessor
from engine.utils.html import ensure_full_document, load_and_inject
from engine.utils.screenshot import html_to_png, is_available as playwright_available

logger = logging.getLogger(__name__)


class PngProcessor(FormatProcessor):
    """Render HTML content to PNG via Playwright screenshot.

    If Playwright is not available, saves the HTML source as fallback.
    """

    def __init__(self, width: int = 1200, height: int = 800, scale: float = 2.0):
        self.width = width
        self.height = height
        self.scale = scale

    def process(
            self,
            content: Any,
            doc_id: str,
            output_dir: Path,
            template_path: str | None = None,
            metadata: dict | None = None,
        ) -> Path:
            logger.info(f"PngProcessor [{doc_id}]: content type={type(content).__name__}, template_path={template_path}")
            self._ensure_dir(output_dir)

            # Build explicit filename from doc_name
            doc_name = (metadata or {}).get("doc_name", doc_id)
            slug = doc_id.lower()
            name_slug = self._slugify(doc_name)
            base_name = f"{slug}_{name_slug}_visual"

            # ── Ensure dict if JSON string ──
            if isinstance(content, str) and template_path:
                content = self._try_parse_json(content, doc_id)

            # ── Build HTML ──
            if isinstance(content, dict) and template_path:
                # Template injection mode (LLM_THEN_RENDER)
                html = load_and_inject(Path(template_path), content)
            elif isinstance(content, dict):
                # JSON but no template — render as styled card
                html = self._json_to_styled_html(content, doc_id)
            elif isinstance(content, str):
                html = self._strip_fences(content)
            else:
                html = str(content)

            html = ensure_full_document(html)

            # ── Screenshot ──
            png_path = output_dir / f"{base_name}.png"

            if playwright_available():
                success = html_to_png(
                    html, png_path,
                    width=self.width, height=self.height,
                    full_page=True,   # ← add this
                    scale=self.scale,
                )
                if success:
                    return png_path
                
            # Fallback: save HTML source
            logger.warning(
                f"PngProcessor [{doc_id}]: Playwright unavailable or failed. "
                f"Saving HTML source as fallback."
            )
            html_path = output_dir / f"{base_name}.html"
            html_path.write_text(html, encoding="utf-8")
            return html_path
    
    def _try_parse_json(self, content: str, doc_id: str) -> dict | str:
            """Try to parse string as JSON for template injection. Return original string if not JSON."""
            text = content.strip()
            # Strip markdown fences
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[-1].strip() == "```":
                    lines = lines[1:-1]
                else:
                    lines = lines[1:]
                text = "\n".join(lines).strip()
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    logger.info(f"PngProcessor [{doc_id}]: parsed JSON string to dict for template injection")
                    return parsed
            except json.JSONDecodeError:
                logger.warning(f"PngProcessor [{doc_id}]: content is string but not valid JSON, treating as HTML")
            return content
    
    def _json_to_styled_html(self, data: dict, doc_id: str) -> str:
        """Convert a JSON payload to a styled HTML card when no template exists."""
        title = data.get("title", data.get("persona_name", doc_id))
        cards_html = []

        for key, value in data.items():
            if isinstance(value, list):
                items = "".join(f"<li>{v}</li>" for v in value)
                cards_html.append(
                    f'<div class="card-section">'
                    f'<h3>{key.replace("_", " ").title()}</h3>'
                    f'<ul>{items}</ul></div>'
                )
            elif isinstance(value, str) and len(value) > 50:
                cards_html.append(
                    f'<div class="card-section">'
                    f'<h3>{key.replace("_", " ").title()}</h3>'
                    f'<p>{value}</p></div>'
                )

        body = "\n".join(cards_html)
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif;
         margin: 0; padding: 40px; background: #f8f9fa; color: #1a1a1a; }}
  .card {{ background: white; border-radius: 12px; padding: 32px;
           max-width: 1100px; margin: 0 auto;
           box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  h1 {{ font-size: 28px; margin-bottom: 24px; color: #111; }}
  h3 {{ font-size: 16px; color: #555; text-transform: uppercase;
        letter-spacing: 0.5px; margin-bottom: 8px; }}
  .card-section {{ margin-bottom: 20px; padding-bottom: 16px;
                   border-bottom: 1px solid #eee; }}
  ul {{ padding-left: 20px; }}
  li {{ margin-bottom: 4px; }}
</style></head>
<body><div class="card"><h1>{title}</h1>{body}</div></body></html>"""

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