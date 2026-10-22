"""HTML processor: validate, save as self-contained .html file."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from engine.processors.base import FormatProcessor
from engine.utils.html import validate_html, ensure_full_document, extract_html_from_llm

logger = logging.getLogger(__name__)


class HtmlProcessor(FormatProcessor):
    """Process LLM-generated HTML into a clean, self-contained file.
    2. Ensure full document structure
    3. Validate (log warnings for issues)
    4. Save as .html
    """

    def process(self, content, doc_id, output_dir, template_path=None, metadata=None):
        self._ensure_dir(output_dir)

        if isinstance(content, dict):
            from engine.utils.html import load_and_inject
            if template_path:
                html = load_and_inject(Path(template_path), content)
            else:
                import json
                html = f"<pre>{json.dumps(content, indent=2, ensure_ascii=False)}</pre>"
        else:
            html = str(content)
            html = extract_html_from_llm(html)  # ← replaces self._strip_fences(html)

        # Strip markdown code fences if LLM wrapped the HTML
        html = self._strip_fences(html)

        # Ensure full document
        html = ensure_full_document(html)

        # Validate (log-only, don't block)
        issues = validate_html(html)
        if issues:
            logger.warning(f"HtmlProcessor [{doc_id}]: validation issues: {issues}")

        # Build explicit filename from doc_name
        doc_name = (metadata or {}).get("doc_name", doc_id)
        slug = doc_id.lower()
        name_slug = self._slugify(doc_name)
        filename = f"{slug}_{name_slug}_render.html"

        output_path = output_dir / filename
        output_path.write_text(html, encoding="utf-8")
        logger.info(f"HtmlProcessor: wrote {output_path}")

        return output_path

    @staticmethod
    def _strip_fences(text: str) -> str:
        """Remove ```html ... ``` wrapping if present."""
        stripped = text.strip()
        if stripped.startswith("```"):
            lines = stripped.split("\n")
            # Remove first line (```html) and last line (```)
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            return "\n".join(lines).strip()
        return stripped