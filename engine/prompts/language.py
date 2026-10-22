"""Output-language directives.

Every client-facing deliverable is written in English. This module is the single
place that says so, so the rule can be changed once instead of in 30 spec files.
"""

from __future__ import annotations


# Injected into every system prompt.
LANGUAGE_RULES = """## Language and style

**Write 100% of your output in clear, direct English.** The reader is a business
owner who will act on this document, not a marketer grading it.

- Plain business vocabulary. Keep the terms practitioners actually use (SEO, SEA,
  Google Ads, landing page, closing, pipeline, CRM, A/B test, ROI, LTV, CAC).
- Address the reader as "you".
- Money in US dollars by default, formatted `$2,500` or `$12k/mo`. If the client's
  answers clearly use another currency, use theirs consistently.
- Dates written out: `August 12, 2026`.
- Reuse the client's exact vocabulary from their form answers when you write
  about their business.
- Punctuation: use commas, colons, parentheses or full stops. Do not use em
  dashes or en dashes; write ranges with "to" ("10 to 20 clients").
- State things directly. Avoid the "it's not X, it's Y" construction and its
  variants ("not just X, but Y", "rather than X").
"""

# Short reminder for the tail of a prompt, where the last instruction carries
# the most weight.
LANGUAGE_REMINDER = (
    "**Write everything in English** (\"you\", US dollars unless the client uses "
    "another currency, no em dashes)."
)

# One-liner for slim prompts (charts, diagrams, spreadsheets) where every label
# is a couple of words.
LANGUAGE_LABELS = (
    "Write every label, title, header and text string in English "
    "(amounts formatted as `$2,500`)."
)
