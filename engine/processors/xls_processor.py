"""XLSX processor: JSON → styled spreadsheet, or template injection."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from engine.processors.base import FormatProcessor
from engine.utils.excel import create_workbook_from_json, inject_into_template

logger = logging.getLogger(__name__)


class XlsProcessor(FormatProcessor):
    """Transform LLM JSON output into an XLSX file.

    Two modes:
      1. **From scratch** (no template): LLM returns JSON structure → build XLSX
      2. **Template fill**: LLM returns JSON slots → inject into pre-built .xlsx template
    """

    def process(
        self,
        content: Any,
        doc_id: str,
        output_dir: Path,
        template_path: str | None = None,
        metadata: dict | None = None,
    ) -> Path:
        self._ensure_dir(output_dir)
        slug = doc_id.lower()
        doc_name = (metadata or {}).get("doc_name", doc_id)
        name_slug = self._slugify(doc_name)

        # Parse JSON if needed
        data = self._ensure_dict(content)

        if template_path and Path(template_path).exists():
            # Template injection mode
            wb = inject_into_template(Path(template_path), data)
            logger.info(f"XlsProcessor [{doc_id}]: injected into template {template_path}")
        else:
            # Build from scratch
            wb = create_workbook_from_json(data)
            if template_path and not Path(template_path).exists():
                logger.warning(
                    f"XlsProcessor [{doc_id}]: template {template_path} not found, "
                    f"building from JSON."
                )

        filename = f"{slug}_{name_slug}.xlsx"
        output_path = output_dir / filename
        wb.save(str(output_path))
        logger.info(f"XlsProcessor: wrote {output_path}")
        return output_path

    def _ensure_dict(self, content: Any) -> dict:
        """Parse content to dict, handling string JSON and edge cases."""
        if isinstance(content, dict):
            return content

        if isinstance(content, str):
            # Try to parse JSON
            text = content.strip()
            # Strip markdown code fences
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[-1].strip() == "```":
                    lines = lines[1:-1]
                else:
                    lines = lines[1:]
                text = "\n".join(lines).strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                logger.error(f"XlsProcessor: invalid JSON — {e}")
                # Return a minimal structure with the raw text
                return {
                    "sheets": [{
                        "name": "Raw Output",
                        "headers": ["Content"],
                        "rows": [[content[:32000]]],
                    }]
                }

        return {"sheets": [{"name": "Data", "headers": ["Value"], "rows": [[str(content)]]}]}