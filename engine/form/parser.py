"""Parse and validate raw form submissions into typed FormAnswers."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from engine.form.schema import QUESTIONS, QuestionSchema
from engine.models.form import FormAnswers, QuestionType

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    question_id: str
    message: str


@dataclass
class ParseResult:
    answers: FormAnswers | None
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0 and self.answers is not None


class FormParser:
    """Validate and normalize a raw form submission.

    Raw input is a flat dict: {"Q1": "Freelance / independent consultant", "Q7": "I build...", ...}
    Checkbox answers can be a list or comma-separated string.
    """

    def parse(self, raw: dict[str, Any]) -> ParseResult:
        errors: list[ValidationError] = []
        warnings: list[ValidationError] = []
        cleaned: dict[str, str | list[str]] = {}

        # Determine which questions are visible (conditional logic)
        visible = self._resolve_visible_questions(raw)

        for qid, schema in QUESTIONS.items():
            value = raw.get(qid)

            # Skip questions hidden by conditional logic
            if qid not in visible:
                continue

            # ── Required check ──
            if schema.required and not self._has_value(value):
                errors.append(ValidationError(qid, f"{qid} is required but missing or empty"))
                continue

            # Skip if optional and empty
            if not self._has_value(value):
                continue

            # ── Normalize value ──
            normalized = self._normalize(value, schema)

            # ── Type validation ──
            type_error = self._validate_type(qid, normalized, schema)
            if type_error:
                errors.append(type_error)
                continue

            # ── Min length check (textarea/text) ──
            if schema.min_length and isinstance(normalized, str):
                if len(normalized.strip()) < schema.min_length:
                    warnings.append(ValidationError(
                        qid,
                        f"{qid} answer is short ({len(normalized.strip())} chars, "
                        f"recommended {schema.min_length}+). May reduce output quality.",
                    ))

            cleaned[qid] = normalized

        if errors:
            return ParseResult(answers=None, errors=errors, warnings=warnings)

        # Deliverables are always generated in English, regardless of what
        # language the free-text answers happen to be in.
        language = "English"

        answers = FormAnswers(raw=raw, answers=cleaned, language=language)
        return ParseResult(answers=answers, errors=[], warnings=warnings)

    def _resolve_visible_questions(self, raw: dict[str, Any]) -> set[str]:
        """Determine which questions are visible based on conditional logic."""
        visible = set()

        for qid, schema in QUESTIONS.items():
            if schema.conditional_on is None:
                visible.add(qid)
                continue

            # Check all conditions (all must be met)
            all_met = True
            for dep_qid, required_values in schema.conditional_on.items():
                dep_value = raw.get(dep_qid)

                # Special case: "__multiple" means dep question has >1 selection
                if required_values == "__multiple":
                    if isinstance(dep_value, list) and len(dep_value) > 1:
                        continue
                    elif isinstance(dep_value, str) and "," in dep_value:
                        continue
                    else:
                        all_met = False
                        break

                # Normal case: dep_value must be in required_values list
                if isinstance(dep_value, list):
                    # Checkbox: at least one selected option must be in required_values
                    if not any(v in required_values for v in dep_value):
                        all_met = False
                        break
                elif dep_value not in required_values:
                    all_met = False
                    break

            if all_met:
                visible.add(qid)

        return visible

    def _has_value(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True

    def _normalize(self, value: Any, schema: QuestionSchema) -> str | list[str]:
        """Normalize a raw value to the expected type."""

        # Checkbox → always list
        if schema.type == QuestionType.CHECKBOX:
            if isinstance(value, list):
                return [str(v).strip() for v in value if str(v).strip()]
            if isinstance(value, str):
                return [v.strip() for v in value.split(",") if v.strip()]
            return [str(value)]

        # Everything else → string
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        return str(value).strip()

    def _validate_type(
        self, qid: str, value: str | list[str], schema: QuestionSchema
    ) -> ValidationError | None:
        """Validate that the value matches expected type and options."""

        # Option-based types: check against allowed options
        if schema.options and schema.type in (
            QuestionType.DROPDOWN,
            QuestionType.RADIO,
        ):
            if isinstance(value, str) and value not in schema.options:
                # Q24 has dynamic options — skip strict validation
                if qid == "Q24":
                    return None
                return ValidationError(
                    qid,
                    f"{qid} value '{value}' not in allowed options",
                )

        if schema.options and schema.type == QuestionType.CHECKBOX:
            if isinstance(value, list):
                invalid = [v for v in value if v not in schema.options]
                if invalid:
                    return ValidationError(
                        qid,
                        f"{qid} contains invalid options: {invalid}",
                    )

        return None
