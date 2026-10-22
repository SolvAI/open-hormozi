"""Generate inter-document summaries for downstream injection.

After each document is generated, we summarize its key outputs
so downstream docs get focused context, not the full 3000-word doc.
"""

from __future__ import annotations

from engine.models.enums import DocID, Format
from engine.models.outputs import GeneratedDocument


# ─── Summary extraction prompt ───────────────────────────────────

SUMMARY_SYSTEM = """You are a document summarizer for a business strategy pipeline.

Summarize the document in 5-10 bullet points.
Focus ONLY on:
- Key DECISIONS made (what was chosen, what was rejected)
- Specific NUMBERS (prices, targets, scores, timelines)
- NAMES created (offer names, package tiers, guarantee type)
- RECOMMENDATIONS given (what to do, in what order)

Do NOT include:
- Generic principles or frameworks (the downstream doc already knows those)
- Educational content (Part 1 material)
- Verbose descriptions

Be telegraphic. Every bullet should contain a concrete fact or decision.
Write in English.
"""


def build_summary_prompt(doc_id: DocID, doc_content: str) -> tuple[str, str]:
    """Build system + user prompts for summarization.

    Returns: (system_prompt, user_prompt)
    """
    user = (
        f"Summarize this {doc_id.value} document for use by downstream documents "
        f"in the generation pipeline.\n\n"
        f"{doc_content}"
    )

    return SUMMARY_SYSTEM, user


def extract_summary_from_generated(doc: GeneratedDocument) -> str | None:
    """Extract the raw content string from a GeneratedDocument for summarization."""
    # Prefer DOC format, fall back to others
    for fmt in (Format.DOC, Format.HTML, Format.MERMAID):
        asset = doc.assets.get(fmt)
        if asset and asset.succeeded and isinstance(asset.content, str):
            return asset.content
    return None