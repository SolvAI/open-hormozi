"""Main pipeline orchestrator.

Form answers in → diagnostic → documents out, in one pass.

Progress is reported through an optional `on_event` callback, and a run that
stopped early (cancelled, out of credits, invalid key...) can be resumed: the
diagnostic and every finished document are kept on disk and reused, so only
the missing documents are generated again.
"""

from __future__ import annotations

import json
import logging
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional

from engine.models.enums import DocID, Format, GenerationMethod, ModelTier, Channel
from engine.models.form import FormAnswers
from engine.models.diagnostic import DiagnosticOutput, MetaVariables, ChannelScores, ValidationFlag
from engine.models.outputs import GeneratedAsset, GeneratedDocument, PipelineResult
from engine.llm.anthropic_client import AnthropicClient
from engine.llm.retry import ABORT_ERRORS
from engine.form.labels import option_label, question_text
from engine.pipeline.trigger_engine import TriggerEngine
from engine.pipeline.validator import FormValidator
from engine.pipeline.dependency_graph import build_generation_order
from engine.pipeline.context_builder import ContextBuilder
from engine.pipeline.summarizer import build_summary_prompt, extract_summary_from_generated
from engine.prompts.strat_prompt_1 import SYSTEM_PROMPT as STRAT_SYSTEM, build_strat_user_prompt
from engine.prompts.strat_prompt_2 import SYSTEM_PROMPT as EXTRACTOR_SYSTEM, build_extractor_user_prompt
from engine.prompts.fc4_subrouter import resolve_email_sequences
from engine.processors.registry import get_processor
from engine.specs import ALL_SPECS
from engine.utils.html import detect_markdown_in_html, extract_html_from_llm
from engine.utils.file_output import package_output

logger = logging.getLogger(__name__)

# Formats that derive their content from the DOC output (pipeline convention).
_DERIVED_FORMATS = {Format.MERMAID, Format.CHART, Format.PNG, Format.XLS, Format.SLIDES}

# Doc IDs that finished cleanly, so a resumed run can skip them.
_COMPLETED_FILE = "completed_docs.json"

EventCallback = Callable[[dict], None]


class DocumentPipeline:
    """Orchestrate the full generation pipeline for one user."""

    def __init__(
        self,
        client: AnthropicClient,
        output_base: Path = Path("output"),
        on_event: Optional[EventCallback] = None,
    ):
        self.client = client
        self.output_base = output_base
        self._on_event = on_event

    def _emit(self, event_type: str, **data) -> None:
        if self._on_event is None:
            return
        try:
            self._on_event({"type": event_type, **data})
        except Exception as e:  # a broken listener must never kill the run
            logger.warning(f"Progress listener failed on {event_type}: {e}")

    def run(
        self,
        form: FormAnswers,
        user_id: str = "user",
        output_dir: Path | None = None,
        resume: bool = False,
    ) -> PipelineResult:
        """Execute the pipeline.

        Args:
            output_dir: Explicit output path. If None, auto-generates
                        {output_base}/{user_id}_{timestamp}/.
            resume:     Reuse the diagnostic and finished documents already in
                        output_dir and only generate what is missing.
        """

        timestamp = datetime.utcnow()
        if output_dir is None:
            output_dir = self.output_base / f"{user_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(parents=True, exist_ok=True)

        result = PipelineResult(user_id=user_id, timestamp=timestamp, output_dir=output_dir)
        start = time.time()

        try:
            # ── Phase 1: Diagnostic ──
            self._emit("phase", phase="diagnostic")
            if resume and self._has_saved_diagnostic(output_dir):
                logger.info("Phase 1: Restoring saved diagnostic (0 LLM calls)...")
                diagnostic = self._restore_diagnostic(form, output_dir)
            else:
                logger.info("Phase 1: Running diagnostic...")
                diagnostic = self._run_diagnostic(form, output_dir)

            result.diagnostic = diagnostic
            logger.info(
                f"Diagnostic complete: {diagnostic.active_doc_count} docs triggered, "
                f"primary channel: {diagnostic.primary_channel.value}"
            )

            # ── Phase 2: Generate documents ──
            logger.info("Phase 2: Generating documents...")
            generation_order = build_generation_order(diagnostic.triggered_docs)

            from engine.specs import has_spec
            runnable = [d for d in generation_order if has_spec(d)]
            skipped = [d for d in generation_order if not has_spec(d)]
            if skipped:
                logger.info(f"Skipping {len(skipped)} docs without specs: {[d.value for d in skipped]}")
            logger.info(f"Generation order: {[d.value for d in runnable]}")

            completed = self._load_completed(output_dir) if resume else set()
            if resume:
                self._hydrate_completed(result, completed, output_dir)
            else:
                self._save_completed(output_dir, completed)

            self._emit(
                "plan",
                docs=[{"id": d.value, "name": ALL_SPECS[d].name} for d in runnable],
                completed=[d.value for d in runnable if d in completed],
                primary_channel=diagnostic.primary_channel.value,
            )

            ctx_builder = ContextBuilder(form, diagnostic, result)

            for index, doc_id in enumerate(runnable):
                if doc_id in completed:
                    continue
                spec = ALL_SPECS[doc_id]

                self._emit("doc_start", doc=doc_id.value, name=spec.name,
                           index=index, total=len(runnable))
                gen_doc = self._generate_document(doc_id, spec, ctx_builder, output_dir)
                result.add_document(gen_doc)

                # Summarize for downstream
                if spec.downstream_consumers:
                    self._summarize_document(gen_doc, output_dir)

                errors = [
                    f"{fmt.value}: {a.error}" for fmt, a in gen_doc.assets.items() if a.error
                ]
                if gen_doc.all_succeeded:
                    completed.add(doc_id)
                    self._save_completed(output_dir, completed)
                self._emit("doc_done", doc=doc_id.value, name=spec.name,
                           ok=gen_doc.all_succeeded, errors=errors)

            # ── Phase 3: Write manifest ──
            self._write_manifest(result, output_dir)

            # ── Phase 4: Package deliverable ZIP ──
            self._emit("phase", phase="packaging")
            logger.info("Phase 4: Packaging ZIP...")
            zip_path = package_output(output_dir)

            if zip_path.suffix == ".zip":
                logger.info(f"Packaged: {zip_path}")

        except ABORT_ERRORS as e:
            logger.warning(f"Pipeline stopped: {type(e).__name__}: {e}")
            result.fatal_error = e

        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            result.errors.append(str(e))

        result.total_generation_time_s = time.time() - start
        logger.info(
            f"Pipeline complete: {result.doc_count} docs, "
            f"{result.asset_count} assets, "
            f"${result.total_cost_usd:.3f}, "
            f"{result.total_generation_time_s:.1f}s"
        )
        logger.info(f"LLM usage: {self.client.usage.summary()}")

        return result

    # ─── Resume support ──────────────────────────────────────

    @staticmethod
    def _has_saved_diagnostic(output_dir: Path) -> bool:
        diag_dir = output_dir / "diagnostic"
        return (diag_dir / "strat_raw.md").exists() and (diag_dir / "strat_triggers.json").exists()

    @staticmethod
    def _load_completed(output_dir: Path) -> set[DocID]:
        path = output_dir / _COMPLETED_FILE
        if not path.exists():
            return set()
        completed = set()
        for value in json.loads(path.read_text(encoding="utf-8")):
            try:
                completed.add(DocID(value))
            except ValueError:
                logger.warning(f"Unknown doc ID in {_COMPLETED_FILE}: {value}")
        return completed

    @staticmethod
    def _save_completed(output_dir: Path, completed: set[DocID]) -> None:
        (output_dir / _COMPLETED_FILE).write_text(
            json.dumps(sorted(d.value for d in completed)), encoding="utf-8",
        )

    def _restore_diagnostic(self, form: FormAnswers, output_dir: Path) -> DiagnosticOutput:
        """Rebuild DiagnosticOutput from the files a previous run saved, without LLM calls.

        Re-derives deterministic meta-variables and mechanical triggers from
        the form (fast), then reconciles with the stored LLM extraction
        (same logic the original run used).
        """
        # Deterministic baseline (milliseconds, no LLM)
        engine = TriggerEngine(form)
        meta = engine.derive_meta_variables()
        mechanical_triggers = engine.derive_triggers()
        channels = engine.score_channels()

        validator = FormValidator(form)
        flags = validator.run_all()

        diag_dir = output_dir / "diagnostic"
        strat_narrative = (diag_dir / "strat_raw.md").read_text(encoding="utf-8")
        extracted = json.loads((diag_dir / "strat_triggers.json").read_text(encoding="utf-8"))

        return self._reconcile_diagnostic(
            meta=meta,
            channels=channels,
            flags=flags,
            extracted=extracted,
            mechanical=mechanical_triggers,
            strat_narrative=strat_narrative,
            form=form,
        )

    def _hydrate_completed(
        self,
        result: PipelineResult,
        completed: set[DocID],
        output_dir: Path,
    ) -> None:
        """Load finished documents from a previous attempt into this result.

        Creates stub GeneratedDocuments carrying their saved summaries, so
        context_builder.build() finds upstream context via result.get_summary().
        Their files are already in docs/ and get packaged as usual.
        """
        summary_dir = output_dir / "summaries"
        for doc_id in completed:
            spec = ALL_SPECS.get(doc_id)
            stub = GeneratedDocument(
                doc_id=doc_id,
                doc_name=spec.name if spec else doc_id.value,
            )
            summary_path = summary_dir / f"{doc_id.value}_summary.md"
            if summary_path.exists():
                stub.summary = summary_path.read_text(encoding="utf-8")
            result.add_document(stub)

        logger.info(f"Resuming: {len(completed)} documents already finished")

    # ─── Diagnostic Phase ────────────────────────────────────

    def _run_diagnostic(self, form: FormAnswers, output_dir: Path) -> DiagnosticOutput:
        """Run deterministic triggers + LLM strat + extraction."""

        # 1. Deterministic baseline
        engine = TriggerEngine(form)
        meta = engine.derive_meta_variables()
        mechanical_triggers = engine.derive_triggers()
        channels = engine.score_channels()

        # 2. Validation
        validator = FormValidator(form)
        flags = validator.run_all()

        # 3. Format form for LLM
        form_text = self._format_form_for_llm(form)

        # 4. LLM diagnostic reasoning
        strat_response = self.client.call(
            system=STRAT_SYSTEM,
            user_message=build_strat_user_prompt(form_text),
            task="strat_diagnostic",
            task_label="strat_prompt_1",
        )

        # Save raw strat output
        diag_dir = output_dir / "diagnostic"
        diag_dir.mkdir(parents=True, exist_ok=True)
        (diag_dir / "strat_raw.md").write_text(strat_response.content, encoding="utf-8")

        # 5. Extract structured JSON
        extracted = self.client.call_json(
            system=EXTRACTOR_SYSTEM,
            user_message=build_extractor_user_prompt(strat_response.content),
            task="strat_extraction",
            task_label="strat_prompt_2",
        )

        (diag_dir / "strat_triggers.json").write_text(
            json.dumps(extracted, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # 6. Reconcile LLM output with mechanical baseline
        diagnostic = self._reconcile_diagnostic(
            meta=meta,
            channels=channels,
            flags=flags,
            extracted=extracted,
            mechanical=mechanical_triggers,
            strat_narrative=strat_response.content,
            form=form,
        )

        return diagnostic

    def _reconcile_diagnostic(
        self,
        meta: MetaVariables,
        channels: ChannelScores,
        flags: list[ValidationFlag],
        extracted: dict,
        mechanical: dict[DocID, bool],
        strat_narrative: str,
        form: FormAnswers,
    ) -> DiagnosticOutput:
        """Merge LLM extraction with deterministic baseline.

        LLM output takes precedence, but disagreements are logged.
        """

        # Parse LLM triggers
        llm_triggers: dict[DocID, bool] = {}
        for doc_id in DocID:
            llm_val = extracted.get("triggered_docs", {}).get(doc_id.value)
            mech_val = mechanical.get(doc_id, False)

            if llm_val is not None:
                llm_triggers[doc_id] = bool(llm_val)
                # Log disagreements
                if bool(llm_val) != mech_val:
                    logger.info(
                        f"Trigger disagreement on {doc_id.value}: "
                        f"mechanical={mech_val}, LLM={llm_val} (using LLM)"
                    )
            else:
                llm_triggers[doc_id] = mech_val

        # Universal docs are ALWAYS true regardless of LLM output
        for uid in (DocID.U1, DocID.U2, DocID.U3, DocID.U4, DocID.U5,
                     DocID.U6, DocID.U7, DocID.U8, DocID.U9):
            llm_triggers[uid] = True

        # ── Sync primary channel with LLM trigger decisions ──────
        _CHANNEL_TO_DOC = {
            Channel.CH1_SEA: DocID.CH1,
            Channel.CH2_SOCIAL_ADS: DocID.CH2,
            Channel.CH3_COLD_OUTBOUND: DocID.CH3,
            Channel.CH4_ORGANIC_CONTENT: DocID.CH4,
            Channel.CH5_LOCAL_SEO: DocID.CH5,
            Channel.CH6_REFERRAL: DocID.CH6,
            Channel.CH7_MARKETPLACE: DocID.CH7,
        }
        _DOC_TO_CHANNEL = {v: k for k, v in _CHANNEL_TO_DOC.items()}

        primary_doc = _CHANNEL_TO_DOC.get(channels.primary)

        if primary_doc and not llm_triggers.get(primary_doc, False):
            # LLM untriggered the mechanical primary — find what it picked
            triggered_channels = [
                d for d in (DocID.CH1, DocID.CH2, DocID.CH3,
                            DocID.CH4, DocID.CH5, DocID.CH6, DocID.CH7)
                if llm_triggers.get(d, False)
            ]

            if triggered_channels:
                new_primary_doc = max(
                    triggered_channels,
                    key=lambda d: channels.get_score(_DOC_TO_CHANNEL[d]).score,
                )
                new_channel = _DOC_TO_CHANNEL[new_primary_doc]
                logger.warning(
                    f"LLM overrode primary channel: {channels.primary.value} → "
                    f"{new_channel.value} (untriggered {primary_doc.value}, "
                    f"triggered {new_primary_doc.value})"
                )
                channels.primary = new_channel
                if channels.secondary == new_channel:
                    channels.secondary = None
            else:
                # LLM triggered no channel docs — keep mechanical, force-trigger
                logger.warning(
                    f"LLM triggered no channel docs — forcing {primary_doc.value} "
                    f"to match primary channel {channels.primary.value}"
                )
                llm_triggers[primary_doc] = True
        # ── End sync block ───────────────────────────────────────

        # Parse meta from LLM (fall back to mechanical)
        llm_meta = extracted.get("meta", {})
        # Use mechanical meta — it's already properly typed

        # Parse content angles and priority order
        content_angles = extracted.get("content_angles", [])
        priority_raw = extracted.get("priority_order", [])
        priority_order = []
        for p in priority_raw:
            try:
                priority_order.append(DocID(p))
            except ValueError:
                logger.warning(f"Unknown doc ID in priority order: {p}")

        # Parse FC4 sequences
        email_sequences = resolve_email_sequences(llm_triggers, form.answers)

        # Parse validation flags from LLM (merge with mechanical)
        llm_flags_raw = extracted.get("validation_flags", [])
        for lf in llm_flags_raw:
            flags.append(ValidationFlag(
                rule_name=lf.get("rule_name", "llm_flag"),
                severity=lf.get("severity", "info"),
                message=lf.get("message", ""),
                questions_involved=lf.get("questions_involved", []),
                action=lf.get("action", ""),
            ))

        return DiagnosticOutput(
            meta=meta,
            triggered_docs=llm_triggers,
            channels=channels,
            email_sequences=email_sequences,
            validation_flags=flags,
            content_angles=content_angles,
            priority_order=priority_order,
            diagnostic_narrative=strat_narrative,
        )

    # ─── Document Generation Phase ───────────────────────────

    def _generate_document(
        self,
        doc_id: DocID,
        spec,
        ctx_builder: ContextBuilder,
        output_dir: Path,
    ) -> GeneratedDocument:
        """Generate all formats for one document.

        Four-phase pipeline per document:
          1. DOC content — LLM generates HTML (render deferred)
          2. Derived annexes — MERMAID/CHART/PNG/XLS built from DOC HTML
          3. DOC render — branded PDF assembled with embedded visual annexes
          4. Standalone deliverables — HTML/PDF with full context
        """

        gen_doc = GeneratedDocument(doc_id=doc_id, doc_name=spec.name)
        docs_dir = output_dir / "docs"
        prompts_dir = output_dir / "prompts"

        # ── State tracked across phases ──────────────────────
        doc_html_content: str | None = None
        doc_llm_response = None
        doc_start: float = 0.0
        visual_assets: dict[Format, Path] = {}

        # ── Categorize formats into generation phases ────────
        doc_format_spec = None
        doc_processor = None
        derived_formats: list = []
        standalone_formats: list = []

        for format_spec in spec.formats:
            if format_spec.method == GenerationMethod.STATIC:
                template = Path(format_spec.template_path) if format_spec.template_path else None
                file_path = None

                if template and template.exists():
                    docs_dir.mkdir(parents=True, exist_ok=True)
                    dest = docs_dir / template.name
                    shutil.copy2(template, dest)
                    file_path = dest
                    logger.info(f"Static asset copied: {template} → {dest}")

                    # Include static images in visual_assets for DOC embedding for U3, (value equiation png static)
                    if dest.suffix.lower() in (".png", ".jpg", ".jpeg"):
                        if doc_id == DocID.U3:
                            visual_assets[format_spec.format] = dest

                elif template:
                    logger.warning(f"Static asset not found: {template}")

                asset = GeneratedAsset(
                    doc_id=doc_id,
                    format=format_spec.format,
                    content=None,
                    file_path=file_path,
                    is_static=True,
                )
                gen_doc.add_asset(asset)

            elif format_spec.format == Format.DOC:
                try:
                    doc_processor = get_processor(Format.DOC)
                    doc_format_spec = format_spec
                except KeyError:
                    logger.info(f"No processor for DOC yet — skipping {doc_id.value}.doc")

            elif format_spec.format in _DERIVED_FORMATS:
                derived_formats.append(format_spec)

            else:  # HTML, PDF — standalone deliverables
                standalone_formats.append(format_spec)

        # ── Phase 1: DOC content (LLM only — render deferred) ──
        if doc_format_spec:
            doc_start = time.time()

            try:
                ctx = ctx_builder.build(doc_id, Format.DOC)
            except Exception as e:
                logger.error(f"Context build failed for {doc_id.value}.doc: {e}")
                asset = GeneratedAsset(
                    doc_id=doc_id, format=Format.DOC, content=None, error=str(e),
                )
                gen_doc.add_asset(asset)
                doc_format_spec = None  # skip Phase 3
            else:
                prompts_dir.mkdir(parents=True, exist_ok=True)
                (prompts_dir / f"{doc_id.value}_doc_system.md").write_text(
                    ctx.system_prompt, encoding="utf-8",
                )
                (prompts_dir / f"{doc_id.value}_doc_user.md").write_text(
                    ctx.user_prompt, encoding="utf-8",
                )

                try:
                    effective_tier = (
                        doc_format_spec.model_tier
                        if doc_format_spec.model_tier == ModelTier.HEAVY
                        else None
                    )
                    model_config = self.client.router.resolve(
                        doc_id=doc_id,
                        format=Format.DOC,
                        tier_override=effective_tier,
                    )
                    doc_llm_response = self.client.call(
                        system=ctx.system_prompt,
                        user_message=ctx.user_prompt,
                        model_config=model_config,
                        task_label=f"{doc_id.value}_doc",
                    )

                    raw_text = doc_llm_response.content.strip()
                    if raw_text.startswith('{"type": "error"') or raw_text.startswith('{"type":"error"'):
                        raise RuntimeError(f"API returned error as content: {raw_text[:200]}")

                    doc_html_content = doc_llm_response.content

                    # ── Validate: check for markdown contamination ──
                    md_issues = detect_markdown_in_html(doc_html_content)
                    if md_issues:
                        logger.info(
                            f"Markdown detected in {doc_id.value}.doc: "
                            f"{'; '.join(md_issues)} — attempting fix"
                        )
                        fixed = self._fix_markdown_in_doc(doc_id, doc_html_content)
                        if fixed:
                            md_issues_after = detect_markdown_in_html(fixed)
                            if md_issues_after:
                                logger.warning(
                                    f"Markdown still present in {doc_id.value}.doc "
                                    f"after fix: {'; '.join(md_issues_after)}"
                                )
                            else:
                                logger.info(f"Markdown fixed in {doc_id.value}.doc ✓")
                            # Use fixed version either way — it's likely better
                            doc_html_content = fixed

                    logger.info(
                        f"DOC content ready for {doc_id.value} "
                        f"({time.time() - doc_start:.1f}s LLM)"
                    )

                except ABORT_ERRORS:
                    raise
                except Exception as e:
                    logger.error(f"DOC LLM failed for {doc_id.value}: {e}")
                    asset = GeneratedAsset(
                        doc_id=doc_id,
                        format=Format.DOC,
                        content=None,
                        error=str(e),
                        generation_time_s=time.time() - doc_start,
                    )
                    gen_doc.add_asset(asset)
                    logger.info(
                        f"Generated {doc_id.value}.doc ✗ "
                        f"({asset.generation_time_s:.1f}s)"
                    )
                    doc_format_spec = None  # skip Phase 3

        # ── Phase 2: Derived annexes (from DOC content) ──────
        # If DOC failed, doc_html_content is None and annexes
        # fall back to standard context automatically.
        for format_spec in derived_formats:
            self._generate_format(
                doc_id=doc_id,
                spec=spec,
                format_spec=format_spec,
                ctx_builder=ctx_builder,
                docs_dir=docs_dir,
                prompts_dir=prompts_dir,
                gen_doc=gen_doc,
                visual_assets=visual_assets,
                prior_format_output=doc_html_content,
            )

        # ── Phase 3: DOC render (assemble PDF with visual annexes) ──
        if doc_format_spec and doc_html_content is not None:
            render_start = time.time()
            try:
                metadata = {
                    "doc_name": spec.name,
                    "format": Format.DOC.value,
                    "client_label": self._client_label(ctx_builder.form),
                }
                if visual_assets:
                    metadata["visual_assets"] = visual_assets

                file_path = doc_processor.process(
                    content=doc_html_content,
                    doc_id=doc_id.value,
                    output_dir=docs_dir,
                    template_path=doc_format_spec.template_path,
                    metadata=metadata,
                )

                asset = GeneratedAsset(
                    doc_id=doc_id,
                    format=Format.DOC,
                    content=doc_html_content,
                    file_path=file_path,
                    token_count_in=doc_llm_response.tokens_in,
                    token_count_out=doc_llm_response.tokens_out,
                    model_used=doc_llm_response.model,
                    generation_time_s=time.time() - doc_start,
                )

            except Exception as e:
                logger.error(f"DOC render failed for {doc_id.value}: {e}")
                asset = GeneratedAsset(
                    doc_id=doc_id,
                    format=Format.DOC,
                    content=doc_html_content,
                    error=str(e),
                    token_count_in=getattr(doc_llm_response, "tokens_in", None),
                    token_count_out=getattr(doc_llm_response, "tokens_out", None),
                    model_used=getattr(doc_llm_response, "model", None),
                    generation_time_s=time.time() - doc_start,
                )

            gen_doc.add_asset(asset)
            logger.info(
                f"Generated {doc_id.value}.doc "
                f"{'✓' if asset.succeeded else '✗'} "
                f"({asset.generation_time_s:.1f}s)"
            )

        # ── Phase 4: Standalone deliverables (full context) ──
        for format_spec in standalone_formats:
            self._generate_format(
                doc_id=doc_id,
                spec=spec,
                format_spec=format_spec,
                ctx_builder=ctx_builder,
                docs_dir=docs_dir,
                prompts_dir=prompts_dir,
                gen_doc=gen_doc,
            )

        return gen_doc

    def _generate_format(
        self,
        doc_id: DocID,
        spec,
        format_spec,
        ctx_builder: ContextBuilder,
        docs_dir: Path,
        prompts_dir: Path,
        gen_doc: GeneratedDocument,
        visual_assets: dict[Format, Path] | None = None,
        prior_format_output: str | None = None,
    ) -> None:
        """Generate a single non-DOC format (LLM call + processing).

        Used by Phase 2 (derived annexes) and Phase 4 (standalone).
        When *prior_format_output* is provided the context builder uses it
        as the primary context instead of raw form data + diagnostic.
        """

        # Skip formats without a processor yet
        try:
            processor = get_processor(format_spec.format)
        except KeyError:
            logger.info(
                f"No processor for {format_spec.format.value} yet — "
                f"skipping {doc_id.value}.{format_spec.format.value}"
            )
            return

        # Build prompts
        try:
            ctx = ctx_builder.build(
                doc_id,
                format_spec.format,
                prior_format_output=prior_format_output,
            )
        except Exception as e:
            logger.error(
                f"Context build failed for "
                f"{doc_id.value}.{format_spec.format.value}: {e}"
            )
            asset = GeneratedAsset(
                doc_id=doc_id,
                format=format_spec.format,
                content=None,
                error=str(e),
            )
            gen_doc.add_asset(asset)
            return

        # Save prompts for debugging
        prompts_dir.mkdir(parents=True, exist_ok=True)
        prompt_prefix = f"{doc_id.value}_{format_spec.format.value}"
        (prompts_dir / f"{prompt_prefix}_system.md").write_text(
            ctx.system_prompt, encoding="utf-8",
        )
        (prompts_dir / f"{prompt_prefix}_user.md").write_text(
            ctx.user_prompt, encoding="utf-8",
        )

        # Call LLM + process
        start = time.time()
        try:
            effective_tier = (
                format_spec.model_tier
                if format_spec.model_tier == ModelTier.HEAVY
                else None
            )

            model_config = self.client.router.resolve(
                doc_id=doc_id,
                format=format_spec.format,
                tier_override=effective_tier,
            )

            response = self.client.call(
                system=ctx.system_prompt,
                user_message=ctx.user_prompt,
                model_config=model_config,
                task_label=f"{doc_id.value}_{format_spec.format.value}",
            )

            raw_text = response.content.strip()
            if raw_text.startswith('{"type": "error"') or raw_text.startswith('{"type":"error"'):
                raise RuntimeError(f"API returned error as content: {raw_text[:200]}")

            is_json = (
                format_spec.format in (Format.XLS, Format.CHART, Format.SLIDES)
                or format_spec.method == GenerationMethod.LLM_THEN_RENDER
            )

            if is_json:
                content = response.as_json
            else:
                content = response.content

            metadata = {"doc_name": spec.name, "format": format_spec.format.value}

            file_path = processor.process(
                content=content,
                doc_id=doc_id.value,
                output_dir=docs_dir,
                template_path=format_spec.template_path,
                metadata=metadata,
            )

            asset = GeneratedAsset(
                doc_id=doc_id,
                format=format_spec.format,
                content=content,
                file_path=file_path,
                token_count_in=response.tokens_in,
                token_count_out=response.tokens_out,
                model_used=response.model,
                generation_time_s=time.time() - start,
            )

            # Track visual PNGs for DOC embedding (Phase 2 only)
            if visual_assets is not None and file_path and file_path.suffix == ".png":
                visual_assets[format_spec.format] = file_path

        except ABORT_ERRORS:
            raise
        except Exception as e:
            logger.error(
                f"Generation failed for "
                f"{doc_id.value}.{format_spec.format.value}: {e}"
            )
            asset = GeneratedAsset(
                doc_id=doc_id,
                format=format_spec.format,
                content=None,
                error=str(e),
                generation_time_s=time.time() - start,
            )

        gen_doc.add_asset(asset)
        logger.info(
            f"Generated {doc_id.value}.{format_spec.format.value} "
            f"{'✓' if asset.succeeded else '✗'} "
            f"({asset.generation_time_s:.1f}s)"
        )

    # ─── Markdown Fix ────────────────────────────────────────

    def _fix_markdown_in_doc(self, doc_id: DocID, content: str) -> str | None:
        """Attempt to fix markdown contamination in DOC HTML output.

        Makes a single LLM call with HEAVY tier to convert stray markdown
        syntax to proper HTML tags. Returns corrected HTML, or None on failure.
        """
        try:
            response = self.client.call(
                system=(
                    "You are an HTML formatter. Your ONLY job is converting markdown "
                    "formatting to equivalent HTML tags. Do not change, add, or remove "
                    "any content. Do not add <html>, <head>, or <body> wrappers. "
                    "Output ONLY the corrected HTML fragment."
                ),
                user_message=(
                    "The following document should be an HTML fragment but contains "
                    "markdown syntax. Convert ALL markdown to proper HTML tags:\n"
                    "- ## heading → <h2>heading</h2>\n"
                    "- ### heading → <h3>heading</h3>\n"
                    "- **text** → <strong>text</strong>\n"
                    "- *text* → <em>text</em>\n"
                    "- - item → <ul><li>item</li></ul>\n"
                    "- | table | → <table><tr><td>...</td></tr></table>\n"
                    "- ```code``` → <pre><code>code</code></pre>\n\n"
                    "Keep EVERY word of content identical. Only fix formatting.\n"
                    "Output ONLY the corrected HTML — no explanation, no fences.\n\n"
                    f"{content}"
                ),
                tier=ModelTier.HEAVY,
                task_label=f"{doc_id.value}_doc_md_fix",
            )
            return extract_html_from_llm(response.content)
        except ABORT_ERRORS:
            raise
        except Exception as e:
            logger.warning(f"Markdown fix LLM call failed for {doc_id.value}: {e}")
            return None

    # ─── Summarization ───────────────────────────────────────

    def _summarize_document(self, gen_doc: GeneratedDocument, output_dir: Path) -> None:
        """Generate and store a summary for downstream document injection."""
        raw_content = extract_summary_from_generated(gen_doc)
        if not raw_content:
            return

        system, user = build_summary_prompt(gen_doc.doc_id, raw_content)

        try:
            response = self.client.call(
                system=system,
                user_message=user,
                tier=ModelTier.LIGHT,
                task_label=f"{gen_doc.doc_id.value}_summary",
            )
            gen_doc.summary = response.content

            # Save summary
            summary_dir = output_dir / "summaries"
            summary_dir.mkdir(parents=True, exist_ok=True)
            (summary_dir / f"{gen_doc.doc_id.value}_summary.md").write_text(
                response.content, encoding="utf-8"
            )

        except ABORT_ERRORS:
            raise
        except Exception as e:
            logger.warning(f"Summary failed for {gen_doc.doc_id.value}: {e}")
            gen_doc.summary = f"[Summary generation failed: {e}]"

    # ─── Utilities ───────────────────────────────────────────

    @staticmethod
    def _client_label(form: FormAnswers) -> str:
        """Line printed under the title on each document cover.

        The intake form has no business-name field, so the closest identifier is
        the industry (Q2, free text) qualified by the business type (Q1).
        """
        industry = (form.get("Q2") or "").strip()
        kind = option_label((form.get("Q1") or "").strip())
        if industry and kind:
            return f"{industry} · {kind}"
        return industry or kind

    def _format_form_for_llm(self, form: FormAnswers) -> str:
        """Format all form answers as readable text for the strat prompt.

        Stored values are machine keys; they are shown through their display
        labels (see engine/form/labels.py).
        """
        lines = ["## Client Form Answers\n"]
        for qid in sorted(form.answers.keys(), key=lambda q: int(q[1:])):
            val = form.answers[qid]
            if isinstance(val, list):
                display = " · ".join(f"☑ {option_label(v)}" for v in val)
            else:
                display = option_label(val)
            lines.append(f"- **{qid}** — {question_text(qid)}\n  → {display}")
        return "\n".join(lines)

    def _write_manifest(self, result: PipelineResult, output_dir: Path) -> None:
        """Write manifest.json with pipeline metadata."""
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest = result.to_manifest()
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )