"""HTTP API and static UI for the local app."""

from __future__ import annotations

import json
import os
import re
import shutil
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import previews, settings, store
from app.errors import describe
from app.paths import EXAMPLE_FORM, JOBS_DIR, STATIC_DIR, ensure_dirs
from app.worker import Worker
from engine.form.labels import option_label, question_text
from engine.form.parser import FormParser
from engine.form.schema import QUESTIONS
from engine.llm.anthropic_client import AnthropicClient
from engine.llm.retry import LLMError, LLMFatalError
from engine.llm.router import ModelConfig, ModelRouter
from engine.utils.file_output import _HTML_PREFERRED_STEMS, _get_arcname

worker = Worker()

# The form is split into five screens. Every conditional question comes after
# the question it depends on.
STEPS = [
    {"title": "Your business", "subtitle": "Who you are and what you sell."},
    {"title": "How you make money", "subtitle": "Your offer, how the sale happens, and your numbers."},
    {"title": "Your current engine", "subtitle": "How you get clients today and what you already have."},
    {"title": "Where you want to go", "subtitle": "Who you want to reach and the target you're aiming for."},
    {"title": "Your resources", "subtitle": "Budget, time, skills and the things you won't do."},
]
STEP_OF = {
    **{q: 1 for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q8", "Q9", "Q10", "Q11", "Q12")},
    **{q: 2 for q in ("Q7", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19", "Q20", "Q21", "Q22")},
    **{q: 3 for q in ("Q23", "Q24", "Q25", "Q26", "Q27", "Q28", "Q29", "Q30", "Q31", "Q32", "Q33")},
    **{q: 4 for q in ("Q34", "Q35", "Q36", "Q37", "Q38", "Q39", "Q40", "Q41", "Q42", "Q43")},
    **{q: 5 for q in ("Q44", "Q45", "Q46", "Q47", "Q48", "Q49")},
}

_LOCAL_HOSTS = {"localhost", "127.0.0.1", "[::1]", "::1"}
_CSRF_HEADER = "x-openhormozi"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_dirs()
    store.init()
    worker.start()
    yield
    worker.stop()


app = FastAPI(title="OpenHormozi", lifespan=lifespan, docs_url=None, redoc_url=None)


@app.middleware("http")
async def local_only(request: Request, call_next):
    """Refuse requests that didn't come from this app's own page.

    - Host must be localhost: blocks DNS-rebinding attacks from other websites.
    - State-changing API calls must carry a custom header, which a browser only
      sends cross-origin after a CORS preflight this server never approves.
    """
    host = request.headers.get("host", "")
    if not host.endswith("]"):  # strip the port, but not from a bare IPv6 literal
        host = host.rsplit(":", 1)[0]
    if os.environ.get("OPENHORMOZI_ALLOW_ANY_HOST") != "1" and host not in _LOCAL_HOSTS:
        return PlainTextResponse("Forbidden host", status_code=403)
    if (request.url.path.startswith("/api/")
            and request.method not in ("GET", "HEAD", "OPTIONS")
            and request.headers.get(_CSRF_HEADER) != "1"):
        return PlainTextResponse("Missing X-OpenHormozi header", status_code=403)
    return await call_next(request)


@app.middleware("http")
async def revalidate_ui(request: Request, call_next):
    """Browsers re-check the UI's CSS and JS on each load, so an update shows
    up on reload. Unchanged files come back as cheap 304s."""
    response = await call_next(request)
    path = request.url.path
    if path.startswith("/static/") and not path.startswith("/static/fonts/"):
        response.headers["Cache-Control"] = "no-cache"
    return response


def _error(status: int, code: str, detail: str | None = None) -> JSONResponse:
    return JSONResponse({"error": describe(code), "detail": detail}, status_code=status)


# ─── Serialization ──────────────────────────────────────────────

def _elapsed(job: dict) -> float:
    elapsed = job["elapsed_s"]
    if job["status"] == "running" and job["started_at"]:
        started = datetime.fromisoformat(job["started_at"])
        elapsed += (datetime.now(timezone.utc) - started).total_seconds()
    return round(elapsed, 1)


def _public(job: dict, full: bool = False) -> dict:
    docs = job["docs"]
    done = sum(1 for d in docs if d["status"] == "done")
    data = {
        "id": job["id"],
        "name": job["name"],
        "status": job["status"],
        "created_at": job["created_at"],
        "finished_at": job["finished_at"],
        "phase": job["phase"],
        "current": job["current_doc"],
        "doc_total": len(docs),
        "doc_done": done,
        "doc_failed": sum(1 for d in docs if d["status"] == "failed"),
        "cost_usd": round(job["cost_usd"] + job["run_cost_usd"], 3),
        "elapsed_s": _elapsed(job),
        "attempts": job["attempts"],
        "error": describe(job["error_code"]),
        "error_detail": job["error_message"],
        "primary_channel": job["primary_channel"],
        "has_zip": job["has_zip"],
        "resumable": job["status"] in store.RESUMABLE,
        "thumbs": _thumbs(job["id"], docs),
    }
    if full:
        data["docs"] = docs
        data["files"] = _list_files(job["id"])
        data["form"] = job["form"]
        data["diagnosis"] = _diagnosis(job["id"])
    return data


def _list_files(job_id: str) -> list[dict]:
    """The deliverables, grouped like the ZIP (same selection rules)."""
    docs_dir = JOBS_DIR / job_id / "docs"
    if not docs_dir.exists():
        return []
    files = [f for f in docs_dir.iterdir() if f.is_file()]
    pdf_stems = {f.stem for f in files if f.suffix == ".pdf"}
    listed = []
    for f in sorted(files, key=lambda p: p.name.lower()):
        if f.suffix == ".mmd":
            continue
        if f.stem in _HTML_PREFERRED_STEMS:
            if f.suffix == ".pdf":
                continue
        elif f.suffix == ".html" and f.stem in pdf_stems:
            continue
        arcname = _get_arcname(f.name)
        folder = arcname.split("/", 1)[0] if "/" in arcname else "Other"
        stat = f.stat()
        preview = previews.kind_of(f)
        # The reader shows documents as a web page when there's an HTML version
        # (a report's screen copy, a landing page...), with the PDF one click away.
        readable = preview in ("report", "page", "web")
        web, pdf = f.with_suffix(".html"), f.with_suffix(".pdf")
        listed.append({
            "name": f.name,
            "folder": folder,
            "kind": f.suffix.lstrip(".").lower(),
            "size": stat.st_size,
            "v": int(stat.st_mtime),
            "preview": preview,
            "parts": previews.part_count(preview),
            "web": web.name if readable and web.exists() else None,
            "pdf": pdf.name if readable and pdf.exists() else None,
        })
    return listed


def _thumbs(job_id: str, docs: list[dict]) -> list[dict]:
    """Up to three finished visuals (persona card, pricing table, chart...) for the strategy list."""
    docs_dir = JOBS_DIR / job_id / "docs"
    if not docs_dir.exists():
        return []
    order = {d["id"].lower(): i for i, d in enumerate(docs) if d["status"] == "done"}
    picks = []
    for f in docs_dir.glob("*.png"):
        doc = f.stem.split("_", 1)[0].lower()
        if doc in order and f.stem.endswith(("_visual", "_chart")):
            picks.append((order[doc], f.name, int(f.stat().st_mtime)))
    return [{"name": name, "v": v} for _, name, v in sorted(picks)[:3]]


def _diagnosis(job_id: str) -> dict | None:
    """The diagnostic's verdict, once it has run."""
    path = JOBS_DIR / job_id / "diagnostic" / "strat_triggers.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    meta = data.get("meta") or {}
    channels = data.get("channels") or {}
    return {
        "maturity": meta.get("maturity"),
        "bottleneck": meta.get("bottleneck"),
        "primary_channel": channels.get("primary"),
        "secondary_channel": channels.get("secondary"),
    }


def _get_job(job_id: str) -> dict:
    job = store.get(job_id)
    if job is None:
        raise HTTPException(404, "Strategy not found")
    return job


def _default_name(form: dict) -> str:
    industry = str(form.get("Q2") or "").strip()
    kind = option_label(str(form.get("Q1") or "").strip())
    return (industry or kind)[:80] or f"Strategy {datetime.now():%b %d, %Y}"


# ─── Form schema ────────────────────────────────────────────────

@app.get("/api/schema")
def get_schema() -> dict:
    questions = []
    for qid, q in QUESTIONS.items():
        questions.append({
            "id": qid,
            "step": STEP_OF[qid],
            "text": question_text(qid),
            "type": q.type.value,
            "options": [{"value": o, "label": option_label(o)} for o in (q.options or [])],
            "required": q.required,
            "min_length": q.min_length,
            "conditional_on": q.conditional_on,
            "dynamic_from": "Q23" if qid == "Q24" else None,
        })
    questions.sort(key=lambda q: (q["step"], int(q["id"][1:])))
    return {"steps": STEPS, "questions": questions}


@app.get("/api/example")
def get_example() -> dict:
    return json.loads(EXAMPLE_FORM.read_text(encoding="utf-8"))


# ─── Settings ───────────────────────────────────────────────────

class SettingsIn(BaseModel):
    api_key: Optional[str] = None
    clear_api_key: bool = False
    models: Optional[dict[str, str]] = None


@app.get("/api/settings")
def get_settings() -> dict:
    return settings.public_view()


@app.put("/api/settings")
def put_settings(body: SettingsIn):
    if body.api_key and not body.api_key.strip().startswith("sk-"):
        return _error(400, "invalid_api_key", "Anthropic API keys start with sk-ant-.")
    try:
        settings.update(api_key=body.api_key, clear_key=body.clear_api_key, models=body.models)
    except ValueError as e:
        return _error(400, "model_not_found", str(e))
    return settings.public_view()


class KeyTestIn(BaseModel):
    api_key: Optional[str] = None


@app.post("/api/settings/test")
def test_key(body: KeyTestIn):
    """One tiny Haiku call: proves the key works and the account has credit."""
    key = (body.api_key or "").strip() or settings.get_api_key()
    if not key:
        return _error(400, "no_api_key")
    client = AnthropicClient(api_key=key, router=ModelRouter(models={}),
                             retry_config={"max_retries": 0})
    probe = ModelConfig(model_name="claude-haiku-5-5", max_tokens=16,
                        thinking={"type": "disabled"}, effort="low")
    try:
        client.call(system="Reply with the single word OK.", user_message="Ping",
                    model_config=probe, task_label="key_test")
    except LLMFatalError as e:
        return _error(400, e.code, str(e)[:500])
    except LLMError as e:
        return _error(400, "pipeline_error", str(e)[:500])
    return {"ok": True}


# ─── Jobs ───────────────────────────────────────────────────────

class JobIn(BaseModel):
    form: dict[str, Any]
    name: Optional[str] = None


class RenameIn(BaseModel):
    name: str


@app.get("/api/jobs")
def list_jobs() -> list[dict]:
    return [_public(j) for j in store.list_all()]


@app.post("/api/jobs")
def create_job(body: JobIn):
    if not settings.get_api_key():
        return _error(400, "no_api_key")
    parsed = FormParser().parse(body.form)
    if not parsed.is_valid:
        return JSONResponse({
            "error": {"code": "invalid_form", "title": "Some answers are missing",
                      "message": "Fix the highlighted questions, then generate again."},
            "fields": {e.question_id: e.message for e in parsed.errors},
        }, status_code=422)
    name = (body.name or "").strip()[:80] or _default_name(body.form)
    job = store.create(name, body.form)
    worker.wake()
    return _public(job, full=True)


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    data = _public(_get_job(job_id), full=True)
    _warm_previews(job_id, data)
    return data


_PAGE_ORDER = ("u", "ch", "fc", "bm", "mt")


def _warm_previews(job_id: str, data: dict) -> None:
    """Render the previews of finished documents in the background, in the
    order the strategy page shows them, so they're ready when scrolled to."""
    done = {d["id"].lower() for d in data["docs"] if d["status"] == "done"}

    def page_order(doc: str) -> tuple:
        prefix, number = re.match(r"([a-z]+)(\d+)", doc).groups()
        return (_PAGE_ORDER.index(prefix) if prefix in _PAGE_ORDER else 9, int(number))

    docs_dir = JOBS_DIR / job_id / "docs"
    wanted = [f for f in data["files"] if f["parts"] and f["name"].split("_", 1)[0].lower() in done]
    wanted.sort(key=lambda f: page_order(f["name"].split("_", 1)[0].lower()))
    previews.warm([docs_dir / f["name"] for f in wanted])


@app.patch("/api/jobs/{job_id}")
def rename_job(job_id: str, body: RenameIn) -> dict:
    _get_job(job_id)
    name = body.name.strip()[:80]
    if not name:
        raise HTTPException(400, "Name can't be empty")
    store.update(job_id, name=name)
    return _public(_get_job(job_id))


@app.post("/api/jobs/{job_id}/cancel")
def cancel_job(job_id: str) -> dict:
    job = _get_job(job_id)
    if job["status"] == "queued":
        store.cancel_if_queued(job_id)
    elif job["status"] == "running":
        worker.cancel(job_id)
    else:
        raise HTTPException(409, "This strategy isn't running")
    return _public(_get_job(job_id))


@app.post("/api/jobs/{job_id}/resume")
def resume_job(job_id: str):
    _get_job(job_id)
    if not settings.get_api_key():
        return _error(400, "no_api_key")
    if not store.requeue(job_id):
        raise HTTPException(409, "Only stopped or partial strategies can be resumed")
    worker.wake()
    return _public(_get_job(job_id))


@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: str) -> dict:
    job = _get_job(job_id)
    if job["status"] in store.ACTIVE:
        raise HTTPException(409, "Cancel the generation before deleting it")
    store.delete(job_id)
    shutil.rmtree(JOBS_DIR / job_id, ignore_errors=True)
    return {"ok": True}


@app.get("/api/jobs/{job_id}/log", response_class=PlainTextResponse)
def job_log(job_id: str, lines: int = 200) -> str:
    _get_job(job_id)
    path = JOBS_DIR / job_id / "run.log"
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(content[-max(1, min(lines, 2000)):])


@app.get("/api/jobs/{job_id}/download")
def download_zip(job_id: str):
    job = _get_job(job_id)
    path = JOBS_DIR / job_id / "strategy_pack.zip"
    if not path.exists():
        raise HTTPException(404, "No ZIP for this strategy yet")
    slug = re.sub(r"[^a-z0-9]+", "-", job["name"].lower()).strip("-")[:50] or "strategy"
    return FileResponse(path, filename=f"{slug}-strategy.zip", media_type="application/zip")


@app.get("/api/jobs/{job_id}/files/{name}")
def job_file(job_id: str, name: str):
    _get_job(job_id)
    docs_dir = (JOBS_DIR / job_id / "docs").resolve()
    path = (docs_dir / name).resolve()
    if path.parent != docs_dir or not path.is_file():
        raise HTTPException(404, "File not found")
    headers = {}
    if path.suffix == ".html":
        # Generated pages run in a sandbox with their own origin, so their
        # scripts can't reach this app's API, in the reader or in a new tab.
        headers["Content-Security-Policy"] = "sandbox allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms"
    return FileResponse(path, content_disposition_type="inline", filename=path.name, headers=headers)


@app.get("/api/jobs/{job_id}/previews/{name}/{part}")
def job_preview(job_id: str, name: str, part: int):
    _get_job(job_id)
    docs_dir = (JOBS_DIR / job_id / "docs").resolve()
    path = (docs_dir / name).resolve()
    if path.parent != docs_dir or not path.is_file():
        raise HTTPException(404, "File not found")
    kind = previews.kind_of(path)
    if not 0 <= part < previews.part_count(kind):
        raise HTTPException(404, "No preview for this file")
    try:
        out = previews.get(path, kind, part)
    except Exception:
        raise HTTPException(404, "The preview could not be rendered")
    return FileResponse(out, media_type="image/jpeg")


# ─── UI ─────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path(STATIC_DIR) / "index.html", headers={"Cache-Control": "no-store"})
