"""FC4: Email Sequences.

Modular email system — only generates the sequences triggered by
the client's funnel shape. Uses fc4_subrouter for selection.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


FC4_SPEC = DocSpec(
    id=DocID.FC4,
    name="Email Sequences",
    tier=Tier.FUNNEL,
    purpose=(
        "Generate the complete email automation system — only the applicable sequences. "
        "Each sequence has full copy for every email, timing triggers, and branching logic. "
        "Modular: the fc4_subrouter determines which sequences are generated."
    ),
    model_tier=ModelTier.HEAVY,
    sections=[
        SectionSpec(
            name="Sequence Architecture",
            purpose="Map all active sequences and how they connect",
            tone_note="The overview shows how sequences hand off to each other. No orphaned subscribers.",
            static_content=(
                "## Email Sequence Types\n\n"
                "### Sales Funnel Sequences\n"
                "| Sequence | Trigger | Goal | Length |\n"
                "|----------|---------|------|--------|\n"
                "| **Qualified Confirmation** | Prospect books a call | Prepare them for the call | 1-2 emails |\n"
                "| **Not Qualified + Lead Magnet** | Prospect not ready | Nurture with value | 3-5 emails |\n"
                "| **No-Show Recovery** | Missed appointment | Reschedule | 2-3 emails |\n"
                "| **Post-Call (Sold)** | Bought after call | Onboard + delight | 2-3 emails |\n"
                "| **Post-Call (Not Sold)** | Didn't buy after call | Follow up + re-engage | 3-5 emails |\n\n"
                "### Nurture Sequences\n"
                "| Sequence | Trigger | Goal | Length |\n"
                "|----------|---------|------|--------|\n"
                "| **Long-Term Nurture** | Lead not ready to buy | Stay top of mind | Ongoing (weekly/biweekly) |\n\n"
                "### Post-Purchase Sequences\n"
                "| Sequence | Trigger | Goal | Length |\n"
                "|----------|---------|------|--------|\n"
                "| **Post-Purchase Welcome** | Just bought | Onboard, reduce regret | 3-5 emails |\n"
                "| **Abandoned Cart** | Added to cart, didn't buy | Recover the sale | 3 emails |\n\n"
                "### Retention Sequences\n"
                "| Sequence | Trigger | Goal | Length |\n"
                "|----------|---------|------|--------|\n"
                "| **Re-Engagement** | Lapsed customer | Win them back | 3-5 emails |\n"
                "| **Review Request** | Post-delivery satisfaction | Get testimonial | 1-2 emails |\n"
                "| **Referral Ask** | Happy customer | Generate referral | 1-2 emails |\n\n"
                "### Every Sequence Must Have\n"
                "- A defined ENTRY trigger\n"
                "- A defined EXIT (where they go next)\n"
                "- An UNSUBSCRIBE path\n"
                "- A TIMING rule (delays between emails)"
            ),
            dynamic_prompt=(
                "Map the active sequences for this client.\n\n"
                "The fc4_subrouter has determined these sequences are triggered. "
                "List each one with:\n"
                "1. **Entry trigger** (what event starts this sequence)\n"
                "2. **Exit condition** (what ends it — purchased, booked, timed out)\n"
                "3. **Handoff** (where do they go after this sequence ends)\n"
                "4. **Email count** in this sequence\n\n"
                "Present as a flow: 'If X → Sequence A → If bought: Sequence B, If not: Sequence C'"
            ),
        ),
        SectionSpec(
            name="Email Copy (All Active Sequences)",
            purpose="Complete copy for every email in every active sequence",
            tone_note="Each email must be send-ready. No placeholders except [FIRST_NAME] and [PRODUCT_NAME].",
            static_content=(
                "## Email Copy Rules\n\n"
                "1. **Subject lines**: 4-8 words, curiosity or benefit. No ALL CAPS. No 🔥.\n"
                "2. **Preview text**: extends the subject line, doesn't repeat it\n"
                "3. **Body**: plain text preferred. Short paragraphs (2-3 lines). "
                "One idea per email.\n"
                "4. **CTA**: ONE per email. Not 'book a call OR visit our site OR reply.'\n"
                "5. **P.S.**: high-impact line — many people read the P.S. first.\n"
                "6. **Tone**: like writing to ONE person, not an 'audience.'\n"
                "7. **Length**: 100-200 words for transactional, 200-400 for nurture.\n\n"
                "### Personalization\n"
                "- [FIRST_NAME]: always\n"
                "- [COMPANY]: if B2B\n"
                "- [PRODUCT/SERVICE]: if referencing their specific interest\n"
                "- Dynamic content: show different blocks based on segment (if tool supports it)"
            ),
            dynamic_prompt=(
                "Write the complete email copy for ALL active sequences.\n\n"
                "For the triggered sequences, write every email:\n\n"
                "For EACH email:\n"
                "1. **Sequence name** (e.g., 'Post-Call Not Sold')\n"
                "2. **Email number** (e.g., 'Email 2 of 4')\n"
                "3. **Timing** (e.g., 'Day 3 after call')\n"
                "4. **Subject line** (with A/B alternative)\n"
                "5. **Preview text**\n"
                "6. **Full body copy**\n"
                "7. **CTA** (the one action they should take)\n"
                "8. **P.S. line** (optional but recommended)\n\n"
                "All copy in English.\n"
                "Use the client's brand voice from U5.\n"
                "Reference the specific offer from U3 where relevant.\n"
                "Use proof from {Q33} in social proof emails.\n\n"
                "If generating abandoned cart: include product image reference and direct cart link.\n"
                "If generating review request: make the ask specific and include the review link format.\n"
                "If generating referral ask: include the referral incentive from BM5 if available."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate ALL email sequences. "
                "Group by sequence name. "
                "Each email is a complete block: subject, preview, body, CTA, P.S."
            ),
        ),
        FormatSpec(
            format=Format.MERMAID,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate a Mermaid flowchart showing all email sequences and their connections.\n"
                "Nodes = sequences. Arrows = transitions with trigger labels.\n"
                "Show entry points (events) and exit points (outcomes).\n"
                "Quote all labels. Use subgraphs for sequence groups (sales/nurture/retention)."
            ),
        ),
        FormatSpec(
            format=Format.HTML,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate a single self-contained HTML file with inline CSS.\n"
                "Contains 3-4 ready-to-use email templates, each in a styled <div> card.\n"
                "Each card: header with logo placeholder, body with sample copy, "
                "a styled CTA <a> button, and a footer with unsubscribe link.\n"
                "Use <table> layout for email compatibility. All content filled — no placeholders.\n"
                "Do NOT output markdown. Output ONLY valid HTML."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q10", "Q11", "Q13", "Q14",
        "Q16", "Q30", "Q33",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5, DocID.BM1, DocID.BM2, DocID.BM5, DocID.FC2],
    downstream_consumers=[DocID.U6, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Fewer sequences (2-3 max). Simple automation. Focus on the post-lead and post-sale sequences.",
        Maturity.GROWING: "Full sequence set. Automate everything that's currently manual.",
        Maturity.ESTABLISHED: "Advanced: segmentation, dynamic content, behavioral triggers.",
        Maturity.PIVOT: "New sequences for new audience. Repurpose old email knowledge.",
    },
    bottleneck_adaptations={
        Bottleneck.LEAD_GENERATION: "Not-qualified nurture and lead magnet delivery are priority sequences.",
        Bottleneck.CONVERSION: "Post-call follow-up and no-show recovery are priority sequences.",
        Bottleneck.RETENTION: "Re-engagement, review request, and referral ask are priorities.",
        Bottleneck.VISIBILITY: "Standard depth — emails go to existing contacts.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Qualification confirmation sequence must reinforce fit.",
    },
    quality_rules=[
        "Every email must be COMPLETE — subject line, preview text, body, CTA, P.S.",
        "Subject lines: 4-8 words. No clickbait, no ALL CAPS, no excessive emojis.",
        "Each email has ONE CTA. Not two, not three. One.",
        "Sequences must have defined entry and exit — no subscribers stuck in limbo.",
        "Unsubscribe path must exist in every email (legal requirement).",
        "The Mermaid diagram must show how sequences connect to each other.",
        "Only generate sequences that are actually triggered by the fc4_subrouter.",
    ],
)