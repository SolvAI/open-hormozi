"""Filesystem locations. Everything the app writes lives under DATA_DIR."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = Path(os.environ.get("OPENHORMOZI_DATA_DIR", ROOT / "data")).resolve()
JOBS_DIR = DATA_DIR / "jobs"
DB_PATH = DATA_DIR / "openhormozi.db"
SETTINGS_PATH = DATA_DIR / "settings.json"
CONFIG_PATH = ROOT / "config.yaml"
STATIC_DIR = Path(__file__).resolve().parent / "static"
EXAMPLE_FORM = ROOT / "examples" / "example_form.json"


def ensure_dirs() -> None:
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
