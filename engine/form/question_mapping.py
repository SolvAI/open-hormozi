"""Bidirectional mapping between questions and documents.

Two directions:
  - question → docs: "Which docs use Q7?"     (from schema.maps_to)
  - doc → questions: "Which Qs does U3 need?" (from specs.relevant_questions)

Both are useful:
  - question→docs: when a form answer changes, which docs are affected
  - doc→questions: when building a prompt, which answers to inject
"""

from __future__ import annotations

from engine.form.schema import QUESTIONS
from engine.models.enums import DocID


class QuestionMapping:
    """Bidirectional index between question IDs and document IDs."""

    def __init__(self):
        self._q_to_docs: dict[str, set[str]] = {}
        self._doc_to_qs: dict[str, set[str]] = {}
        self._build_from_schema()

    def _build_from_schema(self):
        """Build index from question schema maps_to fields."""
        for qid, schema in QUESTIONS.items():
            self._q_to_docs[qid] = set(schema.maps_to)
            for doc_id_str in schema.maps_to:
                self._doc_to_qs.setdefault(doc_id_str, set()).add(qid)

    def enrich_from_specs(self, specs: dict[str, any]):
        """Merge in relevant_questions from DocSpecs (additive, not replacing).

        Call this after specs are loaded to capture any mappings
        defined in specs but not in schema.
        """
        for doc_id_str, spec in specs.items():
            for qid in spec.relevant_questions:
                self._doc_to_qs.setdefault(doc_id_str, set()).add(qid)
                self._q_to_docs.setdefault(qid, set()).add(doc_id_str)

    # ─── Question → Documents ───

    def docs_for_question(self, question_id: str) -> set[str]:
        """Which documents use this question's answer?"""
        return self._q_to_docs.get(question_id, set())

    # ─── Document → Questions ───

    def questions_for_doc(self, doc_id: str | DocID) -> set[str]:
        """Which questions are relevant to this document?"""
        key = doc_id.value if isinstance(doc_id, DocID) else doc_id
        return self._doc_to_qs.get(key, set())

    def questions_for_doc_sorted(self, doc_id: str | DocID) -> list[str]:
        """Same as above but sorted by question number (Q1, Q2, ... Q49)."""
        qs = self.questions_for_doc(doc_id)
        return sorted(qs, key=lambda q: int(q[1:]))

    # ─── Bulk operations ───

    def relevant_answers(
        self,
        doc_id: str | DocID,
        form_answers: dict[str, any],
    ) -> dict[str, any]:
        """Extract only the form answers relevant to a given document."""
        relevant_qs = self.questions_for_doc(doc_id)
        return {
            qid: form_answers[qid]
            for qid in relevant_qs
            if qid in form_answers and form_answers[qid]
        }

    def impact_of_answer(self, question_id: str) -> list[str]:
        """Which documents would be affected if this answer changes?
        Useful for incremental re-generation."""
        return sorted(
            self.docs_for_question(question_id),
            key=lambda d: (
                0 if d.startswith("U") else
                1 if d.startswith("BM") else
                2 if d.startswith("CH") else
                3 if d.startswith("FC") else 4
            ),
        )

    # ─── Stats ───

    def coverage_report(self) -> dict:
        """Which questions are used by how many docs, and vice versa."""
        return {
            "questions_unused": [
                qid for qid, docs in self._q_to_docs.items()
                if not docs
            ],
            "docs_with_no_questions": [
                did for did, qs in self._doc_to_qs.items()
                if not qs
            ],
            "most_connected_questions": sorted(
                self._q_to_docs.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )[:10],
            "most_connected_docs": sorted(
                self._doc_to_qs.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )[:10],
        }