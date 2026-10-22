"""Base class for all format processors."""

from __future__ import annotations

import re
import unicodedata
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FormatProcessor(ABC):
    """Transform raw LLM output into a final file on disk.

    Each processor handles one output format (doc, xls, png, etc.).
    Input is always the raw LLM response (string or parsed dict).
    Output is always a file path.
    """

    @abstractmethod
    def process(
        self,
        content: Any,
        doc_id: str,
        output_dir: Path,
        template_path: str | None = None,
        metadata: dict | None = None,
    ) -> Path:
        """Process LLM output into a final file.

        Args:
            content: Raw LLM output (markdown string, JSON dict, HTML string, etc.)
            doc_id: Document identifier (e.g., "U3") — used for filename
            output_dir: Directory to write the file into
            template_path: Optional template file to inject content into
            metadata: Optional extra context (doc_name, format_spec, etc.)

        Returns:
            Path to the generated file
        """
        ...

    def _ensure_dir(self, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert a human-readable name to a filesystem-safe lowercase slug.

        Accents are folded rather than stripped — accented document names would
        otherwise produce filenames like `offre_irrsistible`.
        """
        folded = unicodedata.normalize("NFKD", text.lower())
        folded = "".join(c for c in folded if not unicodedata.combining(c))
        slug = folded.replace("œ", "oe").replace("æ", "ae")
        slug = slug.replace(" ", "_").replace("'", "_").replace("&", "and")
        slug = re.sub(r"[^a-z0-9_]", "", slug)
        return re.sub(r"_+", "_", slug).strip("_")