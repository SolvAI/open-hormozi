from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from engine.models.enums import (
    AmbitionProfile,
    Bottleneck,
    Channel,
    DocID,
    EmailSequence,
    Maturity,
    ResourceProfile,
)


@dataclass
class MetaVariables:
    """The 4 derived meta-variables that shape every document."""

    maturity: Maturity
    maturity_rationale: str

    bottleneck: Bottleneck
    bottleneck_rationale: str

    resource: ResourceProfile
    resource_rationale: str

    ambition: AmbitionProfile
    ambition_rationale: str


@dataclass
class ChannelScore:
    """Score breakdown for one channel."""

    channel: Channel
    score: int                             # 0-100
    factors_positive: list[str]            # why it scored high
    factors_negative: list[str]            # why it lost points
    hard_no: bool = False                  # excluded by Q48


@dataclass
class ChannelScores:
    """All 7 channel scores + recommendation."""

    scores: list[ChannelScore]             # all 7
    primary: Channel                       # highest scoring
    secondary: Optional[Channel] = None    # if top 2 within 10 points, or CH7 migration

    def get_score(self, channel: Channel) -> ChannelScore:
        return next(s for s in self.scores if s.channel == channel)

    @property
    def ranked(self) -> list[ChannelScore]:
        return sorted(self.scores, key=lambda s: s.score, reverse=True)


@dataclass
class ValidationFlag:
    """An inconsistency or red flag detected in form answers."""

    rule_name: str          # "revenue_sanity", "budget_vs_ambition", etc.
    severity: str           # "warning", "critical", "info"
    message: str            # human-readable explanation
    questions_involved: list[str]   # ["Q10", "Q19", "Q18"]
    action: str             # what the system does about it


@dataclass
class DiagnosticOutput:
    """Complete output of the strat pipeline (prompts 1 + 2).

    This object drives the entire downstream generation.
    """

    # ─── Meta-variables ───
    meta: MetaVariables

    # ─── Document triggers ───
    triggered_docs: dict[DocID, bool]       # all 31 keys, True/False

    # ─── Channel recommendation ───
    channels: ChannelScores

    # ─── FC4 sub-sequences ───
    email_sequences: list[EmailSequence] = field(default_factory=list)

    # ─── Validation ───
    validation_flags: list[ValidationFlag] = field(default_factory=list)

    # ─── Strategic context (flows into all docs) ───
    content_angles: list[str] = field(default_factory=list)      # 5-8 key angles
    priority_order: list[DocID] = field(default_factory=list)     # most important first
    diagnostic_narrative: str = ""                                 # raw strat prompt 1 output

    # ─── Convenience ───

    @property
    def active_docs(self) -> list[DocID]:
        """Only the triggered doc IDs, in priority order if available."""
        active = [doc_id for doc_id, triggered in self.triggered_docs.items() if triggered]
        if self.priority_order:
            # Return in priority order, with any unranked docs appended
            ordered = [d for d in self.priority_order if d in active]
            remaining = [d for d in active if d not in ordered]
            return ordered + remaining
        return active

    @property
    def active_doc_count(self) -> int:
        return len(self.active_docs)

    @property
    def primary_channel(self) -> Channel:
        return self.channels.primary

    @property
    def has_critical_flags(self) -> bool:
        return any(f.severity == "critical" for f in self.validation_flags)

    def is_triggered(self, doc_id: DocID) -> bool:
        return self.triggered_docs.get(doc_id, False)

    def get_flags_for_doc(self, doc_id: DocID) -> list[ValidationFlag]:
        """Flags relevant to a specific document (loose match on questions)."""
        from engine.specs import ALL_SPECS
        spec = ALL_SPECS.get(doc_id)
        if not spec:
            return []
        relevant_qs = set(spec.relevant_questions)
        return [f for f in self.validation_flags
                if set(f.questions_involved) & relevant_qs]