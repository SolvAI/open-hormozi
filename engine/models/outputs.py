from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from engine.models.enums import DocID, Format
from engine.models.diagnostic import DiagnosticOutput


@dataclass
class GeneratedAsset:
    """One output file (one format of one document)."""

    doc_id: DocID
    format: Format
    content: Any                          # raw LLM output (str, dict, etc.)
    file_path: Optional[Path] = None      # set after processor writes to disk
    token_count_in: int = 0               # prompt tokens
    token_count_out: int = 0              # completion tokens
    model_used: str = ""
    generation_time_s: float = 0.0
    error: Optional[str] = None           # if generation failed
    is_static: bool = False               # True for STATIC assets (no LLM)

    @property
    def succeeded(self) -> bool:
        if self.error is not None:
            return False
        # Static assets succeed if they have a valid file path
        if self.is_static:
            return self.file_path is not None
        return self.content is not None

    @property
    def cost_estimate_usd(self) -> float:
        """Rough cost estimate based on Claude pricing."""
        # Adjust rates as pricing changes
        rates = {
            "opus": (15.0 / 1_000_000, 75.0 / 1_000_000),
            "sonnet": (3.0 / 1_000_000, 15.0 / 1_000_000),
            "haiku": (0.25 / 1_000_000, 1.25 / 1_000_000),
        }
        tier = "sonnet"  # default
        for key in rates:
            if key in self.model_used.lower():
                tier = key
                break
        in_rate, out_rate = rates[tier]
        return (self.token_count_in * in_rate) + (self.token_count_out * out_rate)


@dataclass
class GeneratedDocument:
    """All assets for one document (multiple formats)."""

    doc_id: DocID
    doc_name: str
    assets: dict[Format, GeneratedAsset] = field(default_factory=dict)
    summary: str = ""                     # inter-doc summary for downstream injection

    def add_asset(self, asset: GeneratedAsset):
        self.assets[asset.format] = asset

    @property
    def formats_generated(self) -> list[Format]:
        return [fmt for fmt, asset in self.assets.items() if asset.succeeded]

    @property
    def all_succeeded(self) -> bool:
        return all(a.succeeded for a in self.assets.values())

    @property
    def total_cost_usd(self) -> float:
        return sum(a.cost_estimate_usd for a in self.assets.values())

    @property
    def total_time_s(self) -> float:
        return sum(a.generation_time_s for a in self.assets.values())


@dataclass
class PipelineResult:
    """Complete output of one pipeline run for one user."""

    # ─── Identity ───
    user_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # ─── Inputs ───
    diagnostic: Optional[DiagnosticOutput] = None

    # ─── Outputs ───
    documents: dict[DocID, GeneratedDocument] = field(default_factory=dict)

    # ─── Pipeline metadata ───
    output_dir: Optional[Path] = None
    total_generation_time_s: float = 0.0
    errors: list[str] = field(default_factory=list)

    # ─── Abort ───
    # LLMFatalError or GenerationCancelled that stopped the run early.
    fatal_error: Optional[Exception] = None

    def add_document(self, doc: GeneratedDocument):
        self.documents[doc.doc_id] = doc

    @property
    def doc_count(self) -> int:
        return len(self.documents)

    @property
    def asset_count(self) -> int:
        return sum(len(d.assets) for d in self.documents.values())

    @property
    def total_cost_usd(self) -> float:
        return sum(d.total_cost_usd for d in self.documents.values())

    @property
    def all_succeeded(self) -> bool:
        return all(d.all_succeeded for d in self.documents.values()) and not self.errors

    @property
    def failed_docs(self) -> list[DocID]:
        return [doc_id for doc_id, doc in self.documents.items() if not doc.all_succeeded]

    def get_summary(self, doc_id: DocID) -> str:
        """Get the inter-doc summary for a given doc (used by downstream docs)."""
        doc = self.documents.get(doc_id)
        return doc.summary if doc else ""

    def get_all_file_paths(self) -> list[Path]:
        """All generated file paths for zip packaging."""
        paths = []
        for doc in self.documents.values():
            for asset in doc.assets.values():
                if asset.file_path and asset.succeeded:
                    paths.append(asset.file_path)
        return paths

    def to_manifest(self) -> dict:
        """Generate manifest.json content."""
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "diagnostic": {
                "maturity": self.diagnostic.meta.maturity.value if self.diagnostic else None,
                "bottleneck": self.diagnostic.meta.bottleneck.value if self.diagnostic else None,
                "resource": self.diagnostic.meta.resource.value if self.diagnostic else None,
                "ambition": self.diagnostic.meta.ambition.value if self.diagnostic else None,
                "primary_channel": self.diagnostic.primary_channel.value if self.diagnostic else None,
                "doc_count": self.diagnostic.active_doc_count if self.diagnostic else 0,
            },
            "generation": {
                "total_docs": self.doc_count,
                "total_assets": self.asset_count,
                "total_cost_usd": round(self.total_cost_usd, 4),
                "total_time_s": round(self.total_generation_time_s, 1),
                "all_succeeded": self.all_succeeded,
                "failed": [d.value for d in self.failed_docs],
            },
            "documents": {
                doc_id.value: {
                    "name": doc.doc_name,
                    "formats": [fmt.value for fmt in doc.formats_generated],
                    "cost_usd": round(doc.total_cost_usd, 4),
                    "time_s": round(doc.total_time_s, 1),
                }
                for doc_id, doc in self.documents.items()
            },
        }