
"""Determine which FC4 email sequences to generate.

This is pure logic (no LLM) — derives from triggered docs and form answers.
"""

from __future__ import annotations

from engine.models.enums import DocID, EmailSequence


def resolve_email_sequences(
    triggered_docs: dict[DocID, bool],
    form_answers: dict,
) -> list[EmailSequence]:
    """Determine which email sequences FC4 should generate.

    Rules from FORM.md trigger matrix:
      qualified_confirmation:      BM1 + BM2 triggered
      not_qualified_lead_magnet:   BM1 + FC2 triggered
      no_show_recovery:            BM2 triggered
      post_call_sold:              BM1 triggered
      post_call_not_sold:          BM1 triggered
      long_term_nurture:           FC2 triggered OR Q30 = yes (has email list)
      post_purchase_welcome:       BM6 or BM7 triggered
      abandoned_cart:              BM7 triggered AND Q8 = product
      re_engagement_lapsed:        BM5 triggered
      review_request:              BM5 or BM3 triggered
      referral_ask:                BM5 triggered
    """

    def is_on(doc_id: DocID) -> bool:
        return triggered_docs.get(doc_id, False)

    sequences: list[EmailSequence] = []

    # ── Sales funnel sequences ──
    if is_on(DocID.BM1) and is_on(DocID.BM2):
        sequences.append(EmailSequence.QUALIFIED_CONFIRMATION)

    if is_on(DocID.BM1) and is_on(DocID.FC2):
        sequences.append(EmailSequence.NOT_QUALIFIED_LEAD_MAGNET)

    if is_on(DocID.BM2):
        sequences.append(EmailSequence.NO_SHOW_RECOVERY)

    if is_on(DocID.BM1):
        sequences.append(EmailSequence.POST_CALL_SOLD)
        sequences.append(EmailSequence.POST_CALL_NOT_SOLD)

    # ── Nurture sequences ──
    has_email_list = form_answers.get("Q30", "") in ("Yes — 500+", "Yes — under 500")
    if is_on(DocID.FC2) or has_email_list:
        sequences.append(EmailSequence.LONG_TERM_NURTURE)

    # ── Post-purchase sequences ──
    if is_on(DocID.BM6) or is_on(DocID.BM7):
        sequences.append(EmailSequence.POST_PURCHASE_WELCOME)

    is_product = form_answers.get("Q8", "") in ("Physical product", "Digital product (course, SaaS, template…)")
    if is_on(DocID.BM7) and is_product:
        sequences.append(EmailSequence.ABANDONED_CART)

    # ── Retention sequences ──
    if is_on(DocID.BM5):
        sequences.append(EmailSequence.RE_ENGAGEMENT_LAPSED)
        sequences.append(EmailSequence.REFERRAL_ASK)

    if is_on(DocID.BM5) or is_on(DocID.BM3):
        sequences.append(EmailSequence.REVIEW_REQUEST)

    return sequences