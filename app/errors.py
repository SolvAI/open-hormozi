"""User-facing wording for every way a generation can stop.

The UI shows `title` and `message` in a toast and on the strategy page, with a
button for `action`: "settings" opens Settings, "resume" resumes the run, and
an http(s) URL opens that page.
"""

from __future__ import annotations

CONSOLE_KEYS = "https://console.anthropic.com/settings/keys"
CONSOLE_BILLING = "https://console.anthropic.com/settings/billing"
CONSOLE_LIMITS = "https://console.anthropic.com/settings/limits"

ERRORS: dict[str, dict[str, str]] = {
    "no_api_key": {
        "title": "Add your Anthropic API key",
        "message": "OpenHormozi runs on your own Anthropic account. Paste a key in Settings to start.",
        "action": "settings",
        "action_label": "Open Settings",
    },
    "invalid_api_key": {
        "title": "Anthropic rejected your API key",
        "message": "The key is wrong, revoked or incomplete. Paste a valid key (it starts with sk-ant-) in Settings.",
        "action": "settings",
        "action_label": "Open Settings",
    },
    "permission_denied": {
        "title": "Your key can't use this model",
        "message": "The API key doesn't have access to one of the selected models. Pick another model in Settings, then resume.",
        "action": "settings",
        "action_label": "Open Settings",
    },
    "no_credits": {
        "title": "Your Anthropic credit balance is empty",
        "message": "Add credits in the Anthropic Console, then resume. Every finished document is kept.",
        "action": CONSOLE_BILLING,
        "action_label": "Add credits",
    },
    "spend_limit": {
        "title": "You reached your Anthropic spend limit",
        "message": "Raise the monthly limit in the Anthropic Console, then resume. Every finished document is kept.",
        "action": CONSOLE_LIMITS,
        "action_label": "Open limits",
    },
    "model_not_found": {
        "title": "A selected model isn't available",
        "message": "The model name is unknown or not enabled for your account. Pick another one in Settings, then resume.",
        "action": "settings",
        "action_label": "Open Settings",
    },
    "rate_limited": {
        "title": "Anthropic rate limit reached",
        "message": "Your account hit its rate limit even after several retries. Wait a few minutes, then resume.",
        "action": "resume",
        "action_label": "Resume",
    },
    "overloaded": {
        "title": "Anthropic's API is overloaded",
        "message": "The API kept answering \"overloaded\" after several retries. Wait a few minutes, then resume.",
        "action": "resume",
        "action_label": "Resume",
    },
    "network": {
        "title": "Can't reach the Anthropic API",
        "message": "Check your internet connection, then resume. Your progress is saved.",
        "action": "resume",
        "action_label": "Resume",
    },
    "interrupted": {
        "title": "The app closed during a generation",
        "message": "Resume to continue where it stopped. Finished documents are kept.",
        "action": "resume",
        "action_label": "Resume",
    },
    "pipeline_error": {
        "title": "The generation stopped on an unexpected error",
        "message": "The run log at the bottom of the page has the details. You can resume to try again.",
        "action": "resume",
        "action_label": "Resume",
    },
}


def describe(code: str | None) -> dict[str, str] | None:
    if not code:
        return None
    return {"code": code, **ERRORS.get(code, ERRORS["pipeline_error"])}
