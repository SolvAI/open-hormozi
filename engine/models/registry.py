from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from engine.models.enums import (
    DocID,
    Format,
    GenerationMethod,
    Tier,
    Maturity,
    Bottleneck,
    ModelTier,
)


@dataclass
class SectionSpec:
    """One section within a document's DOC format.

    static_content  → Part 1 (general principles) — injected verbatim, no LLM drift.
    dynamic_prompt  → Part 2 (votre situation) — prompt fragment, placeholders filled at runtime.
    """

    name: str
    purpose: str
    tone_note: str  # how maturity/ambition should shift this section
    static_content: Optional[str] = None
    dynamic_prompt: Optional[str] = None


@dataclass
class FormatSpec:
    """How one output format of a document should be produced."""

    format: Format
    method: GenerationMethod
    template_path: Optional[str] = None       # for TEMPLATE_FILL or LLM_THEN_RENDER
    prompt_fragment: Optional[str] = None      # format-specific LLM instructions
    postprocess: Optional[str] = None          # "screenshot", "excel_inject", "mermaid_validate", etc.
    model_tier: ModelTier = ModelTier.MEDIUM   # which LLM tier to use for this format


@dataclass
class DocSpec:
    """Complete specification for one of the 31 document types.

    This is the single source of truth: prompt source, pipeline config,
    and documentation all in one object.
    """

    id: DocID
    name: str
    tier: Tier
    purpose: str  # 2-3 sentences — WHY this doc exists

    # ─── Content structure (for DOC format) ───
    sections: list[SectionSpec] = field(default_factory=list)

    # ─── Output formats ───
    formats: list[FormatSpec] = field(default_factory=list)

    # ─── Form dependencies ───
    relevant_questions: list[str] = field(default_factory=list)  # ["Q1", "Q7", ...]

    # ─── Document dependencies ───
    upstream_deps: list[DocID] = field(default_factory=list)     # must be generated before this
    downstream_consumers: list[DocID] = field(default_factory=list)  # docs that read this output

    # ─── Per-profile adaptations ───
    maturity_adaptations: dict[Maturity, str] = field(default_factory=dict)
    bottleneck_adaptations: dict[Bottleneck, str] = field(default_factory=dict)

    # ─── Quality rules specific to this doc ───
    quality_rules: list[str] = field(default_factory=list)

    # ─── LLM config ───
    model_tier: ModelTier = ModelTier.MEDIUM  # default tier for DOC format

    def get_format_spec(self, fmt: Format) -> Optional[FormatSpec]:
        """Return the FormatSpec for a given format, or None."""
        return next((f for f in self.formats if f.format == fmt), None)

    @property
    def format_types(self) -> list[Format]:
        return [f.format for f in self.formats]

    @property
    def has_static_template(self) -> bool:
        return any(f.method in (GenerationMethod.TEMPLATE_FILL, GenerationMethod.STATIC) for f in self.formats)

    @property
    def llm_formats(self) -> list[FormatSpec]:
        """Formats that require an LLM call."""
        return [f for f in self.formats if f.method != GenerationMethod.STATIC]