"""Background worker: runs queued jobs one at a time in a thread.

Progress from the pipeline (`on_event`) is written to the job row so the UI can
poll it. Each job also gets its own run.log next to its outputs.
"""

from __future__ import annotations

import logging
import threading
import time

from app import settings, store
from app.paths import JOBS_DIR
from engine.form.parser import FormParser
from engine.llm.anthropic_client import AnthropicClient
from engine.llm.retry import GenerationCancelled, LLMFatalError
from engine.llm.router import ModelRouter
from engine.pipeline.runner import DocumentPipeline

logger = logging.getLogger("openhormozi.worker")

# The per-job run.log needs INFO records from the engine whatever the root
# logger is set to (uvicorn or a test harness may leave it at WARNING).
for _name in ("engine", "openhormozi"):
    logging.getLogger(_name).setLevel(logging.INFO)


class Worker:
    def __init__(self) -> None:
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._cancel_events: dict[str, threading.Event] = {}
        self._thread = threading.Thread(target=self._loop, name="generation-worker", daemon=True)

    # ── Control ──────────────────────────────────────────────

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        for event in self._cancel_events.values():
            event.set()
        self._wake.set()

    def wake(self) -> None:
        self._wake.set()

    def cancel(self, job_id: str) -> bool:
        """Ask a running job to stop. Returns False if it isn't running here."""
        event = self._cancel_events.get(job_id)
        if event is None:
            return False
        event.set()
        return True

    def is_running(self, job_id: str) -> bool:
        return job_id in self._cancel_events

    # ── Loop ─────────────────────────────────────────────────

    def _loop(self) -> None:
        while not self._stop.is_set():
            job = store.claim_next()
            if job is None:
                self._wake.wait(2)
                self._wake.clear()
                continue
            try:
                self._run(job)
            except Exception:  # keep the worker alive whatever happens to one job
                logger.exception(f"[{job['id']}] Worker crashed on this job")
                store.update(job["id"], status="failed", error_code="pipeline_error",
                             error_message="Unexpected worker error, see the app console.",
                             finished_at=store.now_iso())

    def _run(self, job: dict) -> None:
        job_id = job["id"]
        out_dir = JOBS_DIR / job_id
        out_dir.mkdir(parents=True, exist_ok=True)

        cancel_event = threading.Event()
        self._cancel_events[job_id] = cancel_event

        # Per-job log file: only records emitted by this worker thread.
        thread_name = threading.current_thread().name
        handler = logging.FileHandler(out_dir / "run.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        handler.addFilter(lambda record: record.threadName == thread_name)
        logging.getLogger().addHandler(handler)

        resume = job["attempts"] > 1
        docs: list[dict] = job["docs"]
        started = time.time()
        client: AnthropicClient | None = None
        final: dict = {}

        def run_cost() -> float:
            return round(client.usage.total_cost_usd, 4) if client else 0.0

        def on_event(event: dict) -> None:
            kind = event["type"]
            fields: dict = {"run_cost_usd": run_cost()}
            if kind == "phase":
                fields["phase"] = event["phase"]
                fields["current_doc"] = None
            elif kind == "plan":
                done = set(event["completed"])
                docs[:] = [
                    {"id": d["id"], "name": d["name"],
                     "status": "done" if d["id"] in done else "pending", "errors": []}
                    for d in event["docs"]
                ]
                fields.update(docs=docs, phase="documents",
                              primary_channel=event.get("primary_channel"))
            elif kind in ("doc_start", "doc_done"):
                for d in docs:
                    if d["id"] == event["doc"]:
                        if kind == "doc_start":
                            d["status"] = "running"
                            fields["current_doc"] = d["name"]
                        else:
                            d["status"] = "done" if event["ok"] else "failed"
                            d["errors"] = [e[:300] for e in event["errors"]][:5]
                fields["docs"] = docs
            store.update(job_id, **fields)

        try:
            logger.info(f"[{job_id}] Starting {'resumed ' if resume else ''}generation: {job['name']}")
            api_key = settings.get_api_key()
            if not api_key:
                final = {"status": "failed", "error_code": "no_api_key"}
                return

            config = settings.effective_config()
            client = AnthropicClient(
                api_key=api_key,
                router=ModelRouter.from_config(config),
                retry_config=config.get("retry"),
                cancel_event=cancel_event,
            )

            parsed = FormParser().parse(job["form"])
            if not parsed.is_valid:
                errors = "; ".join(f"{e.question_id}: {e.message}" for e in parsed.errors)
                final = {"status": "failed", "error_code": "pipeline_error",
                         "error_message": f"Form validation failed: {errors}"}
                return

            pipeline = DocumentPipeline(client=client, output_base=JOBS_DIR, on_event=on_event)
            result = pipeline.run(form=parsed.answers, user_id=job_id,
                                  output_dir=out_dir, resume=resume)

            error = result.fatal_error
            if isinstance(error, GenerationCancelled):
                final = {"status": "cancelled"}
            elif isinstance(error, LLMFatalError):
                final = {"status": "failed", "error_code": error.code,
                         "error_message": str(error)[:1000]}
            elif result.errors:
                final = {"status": "failed", "error_code": "pipeline_error",
                         "error_message": "; ".join(result.errors)[:1000]}
            elif any(d["status"] == "failed" for d in docs):
                failed = [d["id"] for d in docs if d["status"] == "failed"]
                final = {"status": "partial",
                         "error_message": f"{len(failed)} document(s) had errors: {', '.join(failed)}. "
                                          f"Resume to regenerate them."}
            else:
                final = {"status": "completed"}

        except Exception as e:
            logger.exception(f"[{job_id}] Generation crashed")
            final = {"status": "failed", "error_code": "pipeline_error", "error_message": str(e)[:1000]}

        finally:
            for d in docs:
                if d["status"] == "running":
                    d["status"] = "pending"
            status = final.get("status", "failed")
            zip_ready = status in ("completed", "partial") and (out_dir / "strategy_pack.zip").exists()
            current = store.get(job_id) or job
            store.update(
                job_id,
                **final,
                docs=docs,
                current_doc=None,
                cost_usd=round(current["cost_usd"] + run_cost(), 4),
                run_cost_usd=0,
                elapsed_s=round(current["elapsed_s"] + time.time() - started, 1),
                finished_at=store.now_iso(),
                has_zip=zip_ready,
            )
            logger.info(f"[{job_id}] Finished: {status} (${run_cost():.3f} this attempt)")
            logging.getLogger().removeHandler(handler)
            handler.close()
            self._cancel_events.pop(job_id, None)
