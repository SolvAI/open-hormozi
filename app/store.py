"""SQLite storage for generation jobs.

One row per strategy. A job moves through:
    queued → running → completed | partial | failed | cancelled
and `interrupted` when the app was closed mid-run. Failed, partial, cancelled
and interrupted jobs can be resumed, which puts them back in the queue.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from typing import Any

from app.paths import DB_PATH, DATA_DIR

_lock = threading.RLock()

RESUMABLE = {"failed", "partial", "cancelled", "interrupted"}
ACTIVE = {"queued", "running"}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    status          TEXT NOT NULL,
    form_json       TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    started_at      TEXT,
    finished_at     TEXT,
    phase           TEXT,
    docs_json       TEXT NOT NULL DEFAULT '[]',
    current_doc     TEXT,
    cost_usd        REAL NOT NULL DEFAULT 0,   -- finished attempts
    run_cost_usd    REAL NOT NULL DEFAULT 0,   -- attempt in progress
    elapsed_s       REAL NOT NULL DEFAULT 0,   -- finished attempts
    attempts        INTEGER NOT NULL DEFAULT 0,
    error_code      TEXT,
    error_message   TEXT,
    primary_channel TEXT,
    has_zip         INTEGER NOT NULL DEFAULT 0
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with _lock, _connect() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript(_SCHEMA)
        # A job still marked running belongs to a process that is gone.
        conn.execute(
            "UPDATE jobs SET status='interrupted', error_code='interrupted', "
            "cost_usd=cost_usd+run_cost_usd, run_cost_usd=0, current_doc=NULL, "
            "finished_at=? WHERE status='running'",
            (now_iso(),),
        )


def _row(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    job = dict(row)
    job["form"] = json.loads(job.pop("form_json"))
    job["docs"] = json.loads(job.pop("docs_json"))
    job["has_zip"] = bool(job["has_zip"])
    return job


def create(name: str, form: dict) -> dict:
    job_id = uuid.uuid4().hex[:12]
    with _lock, _connect() as conn:
        conn.execute(
            "INSERT INTO jobs (id, name, status, form_json, created_at) VALUES (?, ?, 'queued', ?, ?)",
            (job_id, name, json.dumps(form, ensure_ascii=False), now_iso()),
        )
    return get(job_id)


def get(job_id: str) -> dict | None:
    with _lock, _connect() as conn:
        return _row(conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone())


def list_all() -> list[dict]:
    with _lock, _connect() as conn:
        rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    return [_row(r) for r in rows]


def update(job_id: str, **fields: Any) -> None:
    if not fields:
        return
    if "docs" in fields:
        fields["docs_json"] = json.dumps(fields.pop("docs"), ensure_ascii=False)
    if "has_zip" in fields:
        fields["has_zip"] = int(bool(fields["has_zip"]))
    cols = ", ".join(f"{k}=?" for k in fields)
    with _lock, _connect() as conn:
        conn.execute(f"UPDATE jobs SET {cols} WHERE id=?", (*fields.values(), job_id))


def claim_next() -> dict | None:
    """Move the oldest queued job to running and return it."""
    with _lock, _connect() as conn:
        row = conn.execute(
            "SELECT id FROM jobs WHERE status='queued' ORDER BY created_at LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE jobs SET status='running', started_at=?, finished_at=NULL, "
            "error_code=NULL, error_message=NULL, run_cost_usd=0, attempts=attempts+1 "
            "WHERE id=?",
            (now_iso(), row["id"]),
        )
    return get(row["id"])


def requeue(job_id: str) -> bool:
    with _lock, _connect() as conn:
        cur = conn.execute(
            f"UPDATE jobs SET status='queued', error_code=NULL, error_message=NULL, "
            f"finished_at=NULL WHERE id=? AND status IN ({','.join('?' * len(RESUMABLE))})",
            (job_id, *RESUMABLE),
        )
        return cur.rowcount == 1


def cancel_if_queued(job_id: str) -> bool:
    with _lock, _connect() as conn:
        cur = conn.execute(
            "UPDATE jobs SET status='cancelled', finished_at=? WHERE id=? AND status='queued'",
            (now_iso(), job_id),
        )
        return cur.rowcount == 1


def delete(job_id: str) -> None:
    with _lock, _connect() as conn:
        conn.execute("DELETE FROM jobs WHERE id=?", (job_id,))
