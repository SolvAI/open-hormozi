"""Assemble system + assistant prompts for any document generation call.

KEY DESIGN PRINCIPLE: The LLM writes ONLY personalized recommendations.
Static/educational content from specs is provided as REFERENCE CONTEXT
(so the LLM understands the framework) but is NOT reproduced in output.
"""

from __future__ import annotations

from typing import Optional

from engine.models.enums import Format, DocID, GenerationMethod

from engine.models.registry import DocSpec, FormatSpec
from engine.models.form import FormAnswers
from engine.models.diagnostic import DiagnosticOutput
from engine.form.labels import answer_label, question_text
from engine.prompts.fragments import (
    HORMOZI_PRINCIPLES,
    QUALITY_BASELINE,
    FORMAT_INSTRUCTIONS,
)
from engine.prompts.language import (
    LANGUAGE_LABELS,
    LANGUAGE_REMINDER,
    LANGUAGE_RULES,
)

# Formats that get the full doc-style prompt
_FULL_PROMPT_FORMATS = {Format.DOC, Format.HTML, Format.PDF}


class PromptAssembler:
    """Builds system and assistant prompts for document generation."""

    # ─── System Prompt ────────────────────────────────────────

    def build_system_prompt(self, spec: DocSpec, format_spec: FormatSpec) -> str:
        if format_spec.format in _FULL_PROMPT_FORMATS:
            return self._build_full_system_prompt(spec, format_spec)
        else:
            return self._build_slim_system_prompt(spec, format_spec)

    def _build_full_system_prompt(self, spec: DocSpec, format_spec: FormatSpec) -> str:
        """Full prompt for DOC/HTML/PDF."""

        sections_brief = self._format_sections_brief(spec)
        format_instr = FORMAT_INSTRUCTIONS.get(format_spec.format, "")
        quality_rules = self._format_quality_rules(spec)

        return f"""You are a Hormozi-method business strategist generating **{spec.id.value}: {spec.name}**.

## Document Purpose
{spec.purpose}

## Sections to Cover
{sections_brief}

{HORMOZI_PRINCIPLES}

{QUALITY_BASELINE}

{LANGUAGE_RULES}

## Document-Specific Rules
{quality_rules}

## Output Format: {format_spec.format.value.upper()}
{format_instr}
{format_spec.prompt_fragment or ""}

## CRITICAL: Output Rules
- Write ONLY personalized recommendations for THIS client. 100-500 words, NEVER over 800.
- Do NOT reproduce any framework, theory, or educational text. The client already has reference material.
- Jump straight to: "For your business, do X because Y."
- Each section: 2-5 bullet points of specific, actionable recommendations. No preamble.
"""

    def _build_slim_system_prompt(self, spec: DocSpec, format_spec: FormatSpec) -> str:
        """Slim prompt for MERMAID/XLS/PNG/CHART/SLIDES."""

        # ── Pick format instruction based on generation method ──
        if format_spec.method == GenerationMethod.LLM_THEN_RENDER:
            format_instr = self._template_render_instruction(format_spec)
        else:
            format_instr = FORMAT_INSTRUCTIONS.get(format_spec.format, "")

        return f"""You are generating a **{format_spec.format.value.upper()}** asset for document {spec.id.value}: {spec.name}.

## Document Context
{spec.purpose}

## YOUR TASK
Generate ONLY the {format_spec.format.value.upper()} output described below.
Do NOT generate a full document, markdown text, or sections.
Output ONLY the {format_spec.format.value.upper()} content — nothing else.

## Format: {format_spec.format.value.upper()}
{format_instr}

## Language
{LANGUAGE_LABELS}

## Specific Instructions
{format_spec.prompt_fragment or "No additional instructions."}
"""

    def _template_render_instruction(self, format_spec: FormatSpec) -> str:
        """Format instruction for LLM_THEN_RENDER: LLM outputs JSON, code renders it."""
        has_template = bool(format_spec.template_path)

        if has_template:
            return (
                "You are producing DATA (JSON) that will be injected into an HTML template and rendered.\n"
                "Do NOT output HTML, CSS, or markdown.\n"
                "Output ONLY a valid JSON object — no prose, no explanation, no code fences.\n"
                f"Template: {format_spec.template_path}\n"
                "The JSON keys must match what the template expects (see instructions below)."
            )
        else:
            return (
                "You are producing DATA (JSON) that will be rendered into a visual asset.\n"
                "Do NOT output HTML, CSS, or markdown.\n"
                "Output ONLY a valid JSON object — no prose, no explanation, no code fences.\n"
                "Follow the exact JSON structure described in the instructions below."
            )

    # ─── Assistant / User Prompt ──────────────────────────────

    def build_assistant_prompt(
        self,
        spec: DocSpec,
        format_spec: FormatSpec,
        form: FormAnswers,
        diagnostic: DiagnosticOutput,
        upstream_summaries: dict[DocID, str],
        prior_format_output: Optional[str] = None,
    ) -> str:
        if format_spec.format in _FULL_PROMPT_FORMATS:
            return self._build_full_assistant_prompt(
                spec, format_spec, form, diagnostic, upstream_summaries,
            )
        else:
            return self._build_slim_assistant_prompt(
                spec, format_spec, form, diagnostic, upstream_summaries,
                prior_format_output=prior_format_output,
            )

    def _build_full_assistant_prompt(
        self,
        spec: DocSpec,
        format_spec: FormatSpec,
        form: FormAnswers,
        diagnostic: DiagnosticOutput,
        upstream_summaries: dict[DocID, str],
    ) -> str:

        relevant_answers = self._format_relevant_answers(spec, form)
        meta_vars = self._format_meta_variables(diagnostic)
        adaptations = self._format_active_adaptations(spec, diagnostic)
        upstream = self._format_upstream(spec, upstream_summaries)
        reference_context = self._format_reference_context(spec)
        section_instructions = self._format_dynamic_prompts(spec, form, diagnostic)
        flags = self._format_relevant_flags(spec, diagnostic)
        angles = self._format_content_angles(diagnostic)

        format_reminder = ""
        if format_spec.format in _FULL_PROMPT_FORMATS:
            format_reminder = (
                "\n**⚠ OUTPUT FORMAT: Write HTML tags only (<h2>, <h3>, <p>, <ul>, <li>, <table>, <blockquote>, etc.). "
                "Do NOT use markdown syntax (no ##, no **, no ```, no | table | pipes, no - bullet dashes). "
                "The reference context above uses markdown for YOUR reading — your output must be pure HTML fragments.**"
            )

        return f"""Generate **{spec.id.value}: {spec.name}** for this client.

## Client Answers
{relevant_answers}

## Diagnostic Profile
{meta_vars}

## Adaptations for This Client
{adaptations}

{upstream}

{reference_context}

{section_instructions}

{flags}

{angles}

---

**Output 100-500 words. Max 800. Personalized recommendations only — no theory.**
**Every bullet must reference this client's specific situation.**
{LANGUAGE_REMINDER}
{format_reminder}
"""

    def _build_slim_assistant_prompt(
        self,
        spec: DocSpec,
        format_spec: FormatSpec,
        form: FormAnswers,
        diagnostic: DiagnosticOutput,
        upstream_summaries: dict[DocID, str],
        prior_format_output: Optional[str] = None,
    ) -> str:

        # ── Derived mode: DOC HTML is the sole context ───────
        if prior_format_output:
            return f"""Generate the {format_spec.format.value.upper()} asset for **{spec.id.value}: {spec.name}**.

## Source Document (visualize THIS content — do not re-derive or contradict anything)

{prior_format_output}

---

**OUTPUT ONLY the {format_spec.format.value.upper()} content.**
Do not include markdown prose, section headings, or explanations.
{LANGUAGE_LABELS}
"""

        # ── Standard mode: raw form data + diagnostic ────────
        relevant_answers = self._format_relevant_answers(spec, form)
        meta_vars = self._format_meta_variables(diagnostic)
        upstream = self._format_upstream_brief(spec, upstream_summaries)
        key_decisions = self._format_key_decisions(diagnostic)

        return f"""Generate the {format_spec.format.value.upper()} asset for **{spec.id.value}: {spec.name}**.

## Client Context
{relevant_answers}

## Profile
{meta_vars}

## Strategic Decisions (use these — do NOT override)
{key_decisions}

{upstream}

---

**OUTPUT ONLY the {format_spec.format.value.upper()} content.**
Do not include markdown prose, section headings, or explanations.
{LANGUAGE_LABELS}
"""

    # ─── Internal formatters ──────────────────────────────────

    def _format_sections_brief(self, spec: DocSpec) -> str:
        """Brief section list — names and purpose only, no full descriptions."""
        parts = []
        for s in spec.sections:
            parts.append(f"- **{s.name}**: {s.purpose}")
        return "\n".join(parts)

    def _format_quality_rules(self, spec: DocSpec) -> str:
        if not spec.quality_rules:
            return "No additional rules."
        return "\n".join(f"- {r}" for r in spec.quality_rules)

    def _format_relevant_answers(self, spec: DocSpec, form: FormAnswers) -> str:
        """Answers shown through their display labels; stored values are machine keys."""
        lines = []
        for qid in spec.relevant_questions:
            val = form.get(qid)
            if val:
                lines.append(f"- **{qid}** — {question_text(qid)}\n  → {answer_label(val)}")
        return "\n".join(lines) if lines else "No specific answers mapped."

    def _format_meta_variables(self, diag: DiagnosticOutput) -> str:
        m = diag.meta
        return (
            f"- **Maturity**: {m.maturity.value} — {m.maturity_rationale}\n"
            f"- **Bottleneck**: {m.bottleneck.value} — {m.bottleneck_rationale}\n"
            f"- **Resource**: {m.resource.value} — {m.resource_rationale}\n"
            f"- **Ambition**: {m.ambition.value} — {m.ambition_rationale}"
        )

    def _format_active_adaptations(self, spec: DocSpec, diag: DiagnosticOutput) -> str:
        parts = []
        mat_note = spec.maturity_adaptations.get(diag.meta.maturity)
        if mat_note:
            parts.append(f"- **Maturity ({diag.meta.maturity.value})**: {mat_note}")
        bot_note = spec.bottleneck_adaptations.get(diag.meta.bottleneck)
        if bot_note:
            parts.append(f"- **Bottleneck ({diag.meta.bottleneck.value})**: {bot_note}")
        return "\n".join(parts) if parts else "Standard depth — no special adaptations."

    def _format_upstream(self, spec: DocSpec, summaries: dict[DocID, str]) -> str:
        if not spec.upstream_deps:
            return ""
        parts = ["## Key Outputs from Upstream Documents"]
        for dep_id in spec.upstream_deps:
            summary = summaries.get(dep_id, "")
            if summary:
                parts.append(f"\n### From {dep_id.value}:\n{summary}")
        return "\n".join(parts)

    def _format_upstream_brief(self, spec: DocSpec, summaries: dict[DocID, str]) -> str:
        """Upstream context for non-DOC formats — full summaries, not truncated."""
        if not spec.upstream_deps:
            return ""
        parts = ["## Upstream Context"]
        for dep_id in spec.upstream_deps:
            summary = summaries.get(dep_id, "")
            if summary:
                parts.append(f"**{dep_id.value}**: {summary}")
        return "\n".join(parts)

    def _format_reference_context(self, spec: DocSpec) -> str:
        """Inject full static content as REFERENCE context (not to reproduce in output)."""
        blocks = []
        for section in spec.sections:
            if section.static_content:
                blocks.append(
                    f"### Reference for '{section.name}' (DO NOT reproduce — for your context only):\n\n"
                    f"{section.static_content}"
                )
        if not blocks:
            return ""
        return (
            "## Background Reference\n"
            "The following frameworks and principles are provided so you understand the methodology.\n"
            "**Read and internalize them, but do NOT include any of this text in your output.**\n"
            "Your output must be ONLY personalized recommendations referencing the client's data.\n\n"
            + "\n\n---\n\n".join(blocks)
        )

    def _format_dynamic_prompts(
        self,
        spec: DocSpec,
        form: FormAnswers,
        diag: DiagnosticOutput,
    ) -> str:
        parts = ["## Section-by-Section Instructions"]

        for section in spec.sections:
            if not section.dynamic_prompt:
                continue

            filled = section.dynamic_prompt

            for qid in spec.relevant_questions:
                val = form.get(qid, "[not provided]")
                filled = filled.replace(f"{{{qid}}}", answer_label(val))

            filled = filled.replace("{maturity_profile}", diag.meta.maturity.value)
            filled = filled.replace("{bottleneck_profile}", diag.meta.bottleneck.value)
            filled = filled.replace("{resource_profile}", diag.meta.resource.value)
            filled = filled.replace("{ambition_profile}", diag.meta.ambition.value)
            filled = filled.replace("{maturity}", diag.meta.maturity.value)
            filled = filled.replace("{bottleneck}", diag.meta.bottleneck.value)
            filled = filled.replace("{channel}", diag.primary_channel.value)

            triggered_list = ", ".join(d.value for d in diag.active_docs)
            filled = filled.replace("{triggered_doc_list}", triggered_list)

            parts.append(f"\n### '{section.name}' — write 3-5 bullets of specific recommendations:\n{filled}")

        return "\n".join(parts)

    def _format_relevant_flags(self, spec: DocSpec, diag: DiagnosticOutput) -> str:
        flags = diag.get_flags_for_doc(spec.id)
        if not flags:
            return ""
        parts = ["## ⚠ Validation Flags (address in this document)"]
        for f in flags:
            parts.append(f"- **[{f.severity}] {f.rule_name}**: {f.message} → {f.action}")
        return "\n".join(parts)

    def _format_content_angles(self, diag: DiagnosticOutput) -> str:
        if not diag.content_angles:
            return ""
        parts = ["## Key Content Angles to Weave In"]
        for i, angle in enumerate(diag.content_angles, 1):
            parts.append(f"{i}. {angle}")
        return "\n".join(parts)

    def _format_key_decisions(self, diag: DiagnosticOutput) -> str:
        """Inject reconciled diagnostic decisions into slim prompts.

        These are FINAL — the LLM must not re-derive them from form data.
        """
        parts = []
        parts.append(f"- **Primary acquisition channel**: {diag.primary_channel.value}")
        if diag.channels.secondary:
            parts.append(f"- **Secondary channel**: {diag.channels.secondary.value}")
        parts.append(f"- **Bottleneck to solve**: {diag.meta.bottleneck.value}")
        parts.append(f"- **Triggered documents**: {', '.join(d.value for d in diag.active_docs)}")
        if diag.content_angles:
            parts.append(f"- **Key angles**: {'; '.join(diag.content_angles[:5])}")
        return "\n".join(parts)