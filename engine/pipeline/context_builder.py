"""Build the complete context for a document generation call.

Pulls together: relevant form answers, diagnostic data, upstream summaries,
and any doc-specific context into a structured bundle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from engine.models.enums import DocID, Format
from engine.models.form import FormAnswers
from engine.models.registry import DocSpec, FormatSpec
from engine.models.diagnostic import DiagnosticOutput
from engine.models.outputs import PipelineResult
from engine.prompts.assembler import PromptAssembler
from engine.specs import get_spec


@dataclass
class GenerationContext:
    """Everything needed to generate one (doc, format) pair."""

    doc_id: DocID
    spec: DocSpec
    format_spec: FormatSpec
    system_prompt: str
    user_prompt: str


class ContextBuilder:
    """Assemble generation context for each document."""

    def __init__(
        self,
        form: FormAnswers,
        diagnostic: DiagnosticOutput,
        pipeline_result: PipelineResult,
    ):
        self.form = form
        self.diagnostic = diagnostic
        self.result = pipeline_result
        self.assembler = PromptAssembler()

    def build(
        self,
        doc_id: DocID,
        fmt: Format,
        prior_format_output: Optional[str] = None,
    ) -> GenerationContext:
        """Build complete generation context for one (doc, format) pair.

        When *prior_format_output* is provided (e.g. DOC HTML for a derived
        annex), it replaces the raw form answers + diagnostic as the primary
        context in the assistant prompt.  The system prompt is unaffected.
        """
        spec = get_spec(doc_id)
        format_spec = spec.get_format_spec(fmt)

        if not format_spec:
            raise ValueError(
                f"{doc_id.value} has no format spec for {fmt.value}. "
                f"Available: {[f.value for f in spec.format_types]}"
            )

        # Collect upstream summaries
        upstream_summaries: dict[DocID, str] = {}
        for dep_id in spec.upstream_deps:
            summary = self.result.get_summary(dep_id)
            if summary:
                upstream_summaries[dep_id] = summary

        system_prompt = self.assembler.build_system_prompt(spec, format_spec)
        user_prompt = self.assembler.build_assistant_prompt(
            spec=spec,
            format_spec=format_spec,
            form=self.form,
            diagnostic=self.diagnostic,
            upstream_summaries=upstream_summaries,
            prior_format_output=prior_format_output,
        )

        return GenerationContext(
            doc_id=doc_id,
            spec=spec,
            format_spec=format_spec,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )