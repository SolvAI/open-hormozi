from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class QuestionType(str, Enum):
    DROPDOWN = "dropdown"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    TEXT = "text"
    TEXTAREA = "textarea"


@dataclass
class QuestionSchema:
    """Definition of one intake form question."""

    id: str                                    # "Q1", "Q2", ...
    section: int                               # 1-10
    text: str                                  # the question as shown to user
    type: QuestionType
    options: Optional[list[str]] = None        # for dropdown/radio/checkbox
    required: bool = True
    min_length: Optional[int] = None           # for text/textarea
    conditional_on: Optional[dict[str, Any]] = None  # {"Q13": ["always", "usually"]} → only show if Q13 in those values
    maps_to: list[str] = field(default_factory=list)  # doc IDs this feeds into: ["U2", "U5", "CH1"]


@dataclass
class FormAnswers:
    """Validated, typed container for one user's intake form submission.

    Access: answers["Q7"] or answers.get("Q7", default)
    All values are stored as strings or list[str] (for checkbox).
    """

    raw: dict[str, Any]                        # original submission
    answers: dict[str, str | list[str]]        # cleaned & validated
    language: str = "English"                  # deliverable language

    def get(self, question_id: str, default: Any = None) -> Any:
        return self.answers.get(question_id, default)

    def __getitem__(self, question_id: str) -> str | list[str]:
        return self.answers[question_id]

    def get_multiple(self, question_ids: list[str]) -> dict[str, Any]:
        """Pull several answers at once for prompt injection."""
        return {qid: self.answers.get(qid) for qid in question_ids if self.answers.get(qid)}

    def has(self, question_id: str) -> bool:
        val = self.answers.get(question_id)
        if val is None:
            return False
        if isinstance(val, str):
            return len(val.strip()) > 0
        if isinstance(val, list):
            return len(val) > 0
        return False

    # ─── Convenience accessors for frequently used answers ───

    @property
    def business_type(self) -> str:
        return self.get("Q1", "")

    @property
    def industry(self) -> str:
        return self.get("Q2", "")

    @property
    def offer_description(self) -> str:
        return self.get("Q7", "")

    @property
    def deal_size(self) -> str:
        return self.get("Q10", "")

    @property
    def monthly_revenue(self) -> str:
        return self.get("Q18", "")

    @property
    def current_methods(self) -> list[str]:
        val = self.get("Q23", [])
        return val if isinstance(val, list) else [val]

    @property
    def bottleneck_answer(self) -> str:
        return self.get("Q42", "")

    @property
    def hard_nos(self) -> list[str]:
        val = self.get("Q48", [])
        return val if isinstance(val, list) else [val]

    @property
    def proof_level(self) -> str:
        return self.get("Q32", "")

    @property
    def team_size(self) -> str:
        return self.get("Q4", "")

    @property
    def has_physical_location(self) -> bool:
        return self.get("Q6", "") in (
            "Yes — it's central to my business",
            "Yes — but most business happens remotely",
        )

    @property
    def conversation_required(self) -> bool:
        return self.get("Q13", "") in ("Always — they can't buy without a conversation",
                                        "Usually — most do, some buy directly")

    @property
    def is_appointment_based(self) -> bool:
        return self.get("Q14", "") == "Yes"

    @property
    def is_ongoing_service(self) -> bool:
        return self.get("Q15", "") in ("Ongoing — months or years",)

    @property
    def has_repeat_purchase(self) -> bool:
        return self.get("Q11", "") in (
            "Yes — regularly (weekly/monthly)",
            "Yes — occasionally (few times/year)",
        )

    @property
    def is_self_serve(self) -> bool:
        return self.get("Q13", "") in ("Rarely — most buy without talking to me",
                                        "Never — fully self-serve")

    @property
    def is_local(self) -> bool:
        return self.get("Q5", "") in ("Local (city / region)",)

    @property
    def is_b2b(self) -> bool:
        return self.get("Q1", "") in (
            "Freelance / independent consultant",
            "Agency / studio (2-10 people)",
        ) or self.get("Q38", "N/A") not in ("N/A (B2C)", "")