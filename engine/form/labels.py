"""Display labels for the intake form.

Answer values are matched literally throughout the codebase (`trigger_engine.py`
midpoint tables, the `conditional_on` rules in `schema.py`, and the spec files),
so the strings in `schema.py` stay as canonical machine keys and are never
edited. This module maps them to the wording shown in the web form and in the
prompts.

Only values that read badly as-is are listed; everything else is shown verbatim.
"""

from __future__ import annotations

from engine.form.schema import QUESTIONS


# ─── Question text ──────────────────────────────────────────────

QUESTION_LABELS: dict[str, str] = {
    "Q46": "Time vs money: where do you sit?",
    "Q47": "Technical comfort: can you… (select all that apply)",
}


# ─── Answer options ─────────────────────────────────────────────

OPTION_LABELS: dict[str, str] = {
    # Q4
    "Solo — just me": "Solo, just me",
    # Q6
    "Yes — it's central to my business": "Yes, it's central to my business",
    "Yes — but most business happens remotely": "Yes, but most business happens remotely",
    "No — fully remote/online": "No, fully remote / online",
    # Q11
    "Yes — regularly (weekly/monthly)": "Yes, regularly (weekly or monthly)",
    "Yes — occasionally (few times/year)": "Yes, occasionally (a few times a year)",
    "Sometimes — if they have a new need": "Sometimes, when they have a new need",
    "Rarely — mostly one-time": "Rarely, mostly one-time",
    # Q12
    "Yes — clear packages with prices": "Yes, clear packages with prices",
    "Somewhat — I have a general structure but it's flexible": "Somewhat: a general structure, but flexible",
    "No — I quote case by case": "No, I quote case by case",
    "No — I haven't formalized anything": "No, I haven't formalized anything",
    # Q13
    "Always — they can't buy without a conversation": "Always: they can't buy without a conversation",
    "Usually — most do, some buy directly": "Usually: most do, some buy directly",
    "Rarely — most buy without talking to me": "Rarely: most buy without talking to me",
    "Never — fully self-serve": "Never: fully self-serve",
    # Q15
    "Ongoing — months or years": "Ongoing (months or years)",
    "Project-based — defined start/end": "Project-based (defined start and end)",
    # Q17
    "Consumer — decides alone": "Consumer who decides alone",
    # Q23
    "I don't have a system — it's random": "I don't have a system, it's random",
    # Q25
    "Nothing — I haven't tried much yet": "Nothing, I haven't tried much yet",
    # Q27
    "$0 — nothing": "$0 (nothing)",
    # Q28
    "Yes — professional, up to date": "Yes, professional and up to date",
    "Yes — but outdated or basic": "Yes, but outdated or basic",
    # Q30
    "Yes — 500+": "Yes, 500+ subscribers",
    "Yes — under 500": "Yes, under 500 subscribers",
    # Q32
    "Strong — portfolio, testimonials, case studies, media/speaking": "Strong: portfolio, testimonials, case studies, media or speaking",
    "Moderate — some client results, a few testimonials": "Moderate: some client results, a few testimonials",
    "Weak — I have experience but nothing documented": "Weak: I have experience but nothing documented",
    "None — starting from scratch": "None: starting from scratch",
    # Q41
    "No rush — I want sustainable growth": "No rush, I want sustainable growth",
    # Q42
    "Nobody knows I exist — I need visibility": "Nobody knows I exist. I need visibility.",
    "People know me but don't reach out — I need lead generation": "People know me but don't reach out. I need lead generation.",
    "I get leads but can't close them — I need conversion help": "I get leads but can't close them. I need conversion help.",
    "I close but my prices are too low — I need pricing/packaging help": "I close, but my prices are too low. I need pricing and packaging help.",
    "I get clients but they leave or don't come back — I need retention": "I get clients but they leave or don't come back. I need retention.",
    "I have too much work but the wrong kind — I need better positioning": "I have too much work of the wrong kind. I need better positioning.",
    # Q44
    "$0 — bootstrapping": "$0 (bootstrapping)",
    # Q45
    "I want to spend ZERO — automate everything": "ZERO hours, automate everything",
    # Q46
    "I have more time than money — I'll do the work": "More time than money: I'll do the work",
    "Balanced — I can invest some of each": "Balanced: I can invest some of each",
    "I have more money than time — I'll pay for speed": "More money than time: I'll pay for speed",
    "I want to buy a system — don't make me build slowly": "I want to buy a system, not build one slowly",
    # Q47
    "None of the above — I need help with everything": "None of the above, I need help with everything",
    # Q48
    "Nothing — I'm open to everything": "Nothing, I'm open to everything",
}


def question_text(question_id: str) -> str:
    """Display wording of a question. Falls back to the ID if unknown."""
    if question_id in QUESTION_LABELS:
        return QUESTION_LABELS[question_id]
    q = QUESTIONS.get(question_id)
    return q.text if q else question_id


def option_label(value: str) -> str:
    """Display label for a stored answer value.

    Free-text answers pass through untouched: they are already in the
    respondent's own words.
    """
    return OPTION_LABELS.get(value, value)


def answer_label(value: str | list[str]) -> str:
    """Render an answer (single or multi-select) as a display string."""
    if isinstance(value, list):
        return ", ".join(option_label(v) for v in value)
    return option_label(value)
