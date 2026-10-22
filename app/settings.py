"""User settings: the Anthropic API key and the model picked for each role.

Stored as plain JSON in data/settings.json on this computer only. The key is
sent to nobody but the Anthropic API.
"""

from __future__ import annotations

import json
import os
import threading
from typing import Any

import yaml

from app.paths import CONFIG_PATH, DATA_DIR, SETTINGS_PATH

_lock = threading.Lock()

# Models offered in the Settings page, best first within each family.
AVAILABLE_MODELS = [
    {"id": "claude-opus-5-5",   "label": "Claude Opus 5.5",   "price": "$4 / $20 per M tokens"},
    {"id": "claude-sonnet-5-5", "label": "Claude Sonnet 5.5", "price": "$2 / $10 per M tokens"},
    {"id": "claude-haiku-5-5",  "label": "Claude Haiku 5.5",  "price": "$0.10 / $0.50 per M tokens"},
    {"id": "claude-fable-5-1",  "label": "Claude Fable 5.1",  "price": "$10 / $50 per M tokens"},
    {"id": "claude-opus-5",     "label": "Claude Opus 5",     "price": "$5 / $25 per M tokens"},
    {"id": "claude-sonnet-5",   "label": "Claude Sonnet 5",   "price": "$2 / $10 per M tokens"},
]

# Roles shown in the UI, mapped to the pipeline's model tiers (config.yaml).
ROLES = {
    "strategy": {"tiers": ["max", "heavy"],
                 "label": "Strategy model",
                 "help": "Diagnoses the business and writes the hardest documents (offer, funnel, sales playbook)."},
    "writing":  {"tiers": ["medium"],
                 "label": "Writing model",
                 "help": "Writes most of the documents."},
    "summary":  {"tiers": ["light"],
                 "label": "Summary model",
                 "help": "Condenses each document so later ones can build on it."},
}


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        raise ValueError(f"Invalid config format in {CONFIG_PATH}")
    return config


def _read() -> dict:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _write(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SETTINGS_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    if os.name == "posix":
        os.chmod(tmp, 0o600)
    tmp.replace(SETTINGS_PATH)


def get_api_key() -> str | None:
    """Saved key first, then ANTHROPIC_API_KEY from the environment or .env."""
    with _lock:
        key = _read().get("api_key")
    key = key or os.environ.get("ANTHROPIC_API_KEY") or ""
    return key.strip() or None


def key_source() -> str | None:
    with _lock:
        if _read().get("api_key"):
            return "settings"
    return "environment" if os.environ.get("ANTHROPIC_API_KEY") else None


def mask_key(key: str | None) -> str | None:
    if not key:
        return None
    return f"{key[:7]}…{key[-4:]}" if len(key) > 14 else "…"


def role_models() -> dict[str, str]:
    """Model per UI role: saved choice, else the config.yaml default."""
    config_models = load_config().get("models", {})
    with _lock:
        saved = _read().get("models", {})
    return {
        role: saved.get(role) or config_models.get(spec["tiers"][0])
        for role, spec in ROLES.items()
    }


def effective_config() -> dict:
    """config.yaml with the user's model choices applied to each tier."""
    config = load_config()
    models = dict(config.get("models", {}))
    for role, model in role_models().items():
        for tier in ROLES[role]["tiers"]:
            models[tier] = model
    config["models"] = models
    return config


def update(api_key: str | None = None, clear_key: bool = False,
           models: dict[str, Any] | None = None) -> None:
    with _lock:
        data = _read()
        if clear_key:
            data.pop("api_key", None)
        elif api_key:
            data["api_key"] = api_key.strip()
        if models:
            known = {m["id"] for m in AVAILABLE_MODELS}
            saved = data.setdefault("models", {})
            for role, model in models.items():
                if role in ROLES and isinstance(model, str) and model.strip():
                    model = model.strip()
                    if model not in known and not model.startswith("claude-"):
                        raise ValueError(f"Unknown model: {model}")
                    saved[role] = model
        _write(data)


def public_view() -> dict:
    key = get_api_key()
    return {
        "has_api_key": bool(key),
        "api_key_hint": mask_key(key),
        "api_key_source": key_source(),
        "models": role_models(),
        "roles": [{"id": r, "label": s["label"], "help": s["help"]} for r, s in ROLES.items()],
        "available_models": AVAILABLE_MODELS,
    }
