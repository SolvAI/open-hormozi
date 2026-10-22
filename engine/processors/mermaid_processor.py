"""Mermaid diagram processor: validate, fix, save as .mmd, optionally render PNG."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from engine.processors.base import FormatProcessor
from engine.utils.mermaid import validate_and_fix, render_to_png

logger = logging.getLogger(__name__)


class MermaidProcessor(FormatProcessor):
    """Process LLM-generated Mermaid diagrams.

    1. Strip markdown fences if present
    2. Apply auto-fixes (unquoted labels, balance issues)
    3. Save as .mmd text file
    4. Render to PNG with Playwright when available
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
        raw = content if isinstance(content, str) else str(content)

        # Validate and fix
        fixed, fixes = validate_and_fix(raw)
        if fixes:
            logger.info(f"MermaidProcessor [{doc_id}]: applied fixes: {fixes}")

        # Build explicit filename from doc_name
        doc_name = (metadata or {}).get("doc_name", doc_id)
        slug = doc_id.lower()
        name_slug = self._slugify(doc_name)
        base_name = f"{slug}_{name_slug}_diagram"

        # Save .mmd source
        mmd_path = output_dir / f"{base_name}.mmd"
        mmd_path.write_text(fixed, encoding="utf-8")
        logger.info(f"MermaidProcessor: wrote {mmd_path}")

        # Attempt PNG render (non-blocking if Playwright is not available)
        png_path = output_dir / f"{base_name}.png"
        rendered = render_to_png(fixed, png_path)
        if rendered:
            logger.info(f"MermaidProcessor: rendered PNG {png_path}")

        return mmd_path