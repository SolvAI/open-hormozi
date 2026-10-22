"""FC5: Retargeting Strategy.

Re-engage website visitors and warm audiences through paid retargeting
across display, video, and social platforms.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


FC5_SPEC = DocSpec(
    id=DocID.FC5,
    name="Retargeting Strategy",
    tier=Tier.FUNNEL,
    purpose=(
        "Design a retargeting system that re-engages warm audiences with the right message "
        "at the right time. Audience segmentation, creative briefs per segment, "
        "budget allocation, frequency caps, and exclusion rules."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Audience Segmentation",
            purpose="Define retargeting audiences by behavior and intent level",
            tone_note="Different audiences need different messages. Don't retarget everyone the same way.",
            static_content=(
                "## Retargeting Audience Tiers\n\n"
                "| Tier | Audience | Intent | Message Strategy |\n"
                "|------|----------|--------|------------------|\n"
                "| **Tier 1: Hot** | Visited pricing/offer page, started form | High | Urgency, guarantee, CTA |\n"
                "| **Tier 2: Warm** | Visited LP, spent 30s+, viewed multiple pages | Medium | Social proof, value recap |\n"
                "| **Tier 3: Cool** | Visited site briefly, bounced | Low | Education, awareness content |\n"
                "| **Tier 4: Engaged** | Watched 50%+ of video, downloaded LM | Medium-High | Case study, next step |\n\n"
                "### Window Rules\n"
                "- Tier 1: 7-day window (strike while hot)\n"
                "- Tier 2: 14-day window\n"
                "- Tier 3: 30-day window\n"
                "- Tier 4: 14-day window\n\n"
                "### Exclusion Rules (Critical)\n"
                "- ALWAYS exclude existing customers from acquisition retargeting\n"
                "- ALWAYS exclude people who already converted\n"
                "- ALWAYS exclude people who visited but aren't in your ICP (if detectable)\n"
                "- Frequency cap: max 3 impressions/day per person"
            ),
            dynamic_prompt=(
                "Define the retargeting audiences for this client.\n\n"
                "Based on:\n"
                "- Funnel from U6 (what pages/steps exist)\n"
                "- Channel: {channel}\n"
                "- Website: {Q28}\n"
                "- Email list: {Q30}\n"
                "- Social presence: {Q31}\n\n"
                "Produce:\n"
                "1. **Audience definitions** per tier (what behavior defines each)\n"
                "2. **Window duration** per audience\n"
                "3. **Exclusion rules** specific to their funnel\n"
                "4. **Minimum audience size** needed for each tier to be viable\n"
                "5. **Pixel/tracking setup** requirements (what needs to be installed)\n\n"
                "If traffic is currently low (<500 visits/mo): acknowledge and "
                "recommend starting retargeting only after traffic builds."
            ),
        ),
        SectionSpec(
            name="Creative Strategy Per Audience",
            purpose="Different messages for different intent levels",
            tone_note="Hot audiences need urgency. Cool audiences need trust. Don't mix them up.",
            static_content=(
                "## The Creative × Audience Matrix\n\n"
                "| Audience Tier | Ad Goal | Creative Type | Message |\n"
                "|--------------|---------|---------------|--------|\n"
                "| Hot (pricing page) | Close | Testimonial + deadline | 'Still thinking? Here's what [client] achieved…' |\n"
                "| Warm (LP visitor) | Engage | Value recap + proof | 'Remember the [offer]? Here's why it works…' |\n"
                "| Cool (bounced) | Educate | Educational content | Blog post, how-to, industry insight |\n"
                "| Engaged (video/LM) | Convert | Case study + CTA | 'See how [similar business] got [result]' |\n\n"
                "### Creative Fatigue Rules\n"
                "- Rotate creatives every 2 weeks (minimum)\n"
                "- Never show the same ad more than 3× to the same person in a day\n"
                "- Prepare 3-4 creatives per audience tier at launch"
            ),
            dynamic_prompt=(
                "Create creative briefs for each retargeting audience.\n\n"
                "Using:\n"
                "- Messaging from U5\n"
                "- Proof from {Q33}\n"
                "- Offer from U3\n\n"
                "For each audience tier:\n"
                "1. **Ad format** (static / carousel / video)\n"
                "2. **Visual direction** (what the ad shows)\n"
                "3. **Primary text** (full ad copy)\n"
                "4. **Headline** (short)\n"
                "5. **CTA button**\n"
                "6. **Platform placement** (display, social, YouTube…)\n\n"
                "Produce 2 creative variations per tier (for A/B testing)."
            ),
        ),
        SectionSpec(
            name="Budget & Platform Setup",
            purpose="Allocate retargeting budget and configure platforms",
            tone_note="Retargeting should be 10-15% of total ad budget. Small but high-ROAS.",
            static_content=(
                "## Retargeting Budget Rules\n\n"
                "### Budget Allocation\n"
                "- **10-15% of total ad spend** goes to retargeting\n"
                "- If total budget < $1,500/mo: skip retargeting — focus all on prospecting\n"
                "- If total budget $1,500-3,000: basic retargeting (Tier 1 only)\n"
                "- If total budget > $3,000: full tiered retargeting\n\n"
                "### Platform Options\n"
                "| Platform | Best For | Min Budget |\n"
                "|----------|----------|----------|\n"
                "| **Meta (Facebook/Instagram)** | Visual retargeting, social proof ads | $150/mo |\n"
                "| **Google Display Network** | Broad reach, reminder ads | $200/mo |\n"
                "| **YouTube** | Video retargeting (if source content exists) | $300/mo |\n"
                "| **LinkedIn** | B2B retargeting (expensive but precise) | $500/mo |\n\n"
                "### The Setup Checklist\n"
                "- [ ] Pixel/tag installed on all funnel pages\n"
                "- [ ] Custom audiences created per tier\n"
                "- [ ] Exclusion audiences configured\n"
                "- [ ] Frequency caps set\n"
                "- [ ] Creatives uploaded per audience\n"
                "- [ ] Conversion tracking verified"
            ),
            dynamic_prompt=(
                "Design the retargeting budget and platform setup.\n\n"
                "Based on:\n"
                "- Total ad budget: {Q44}\n"
                "- Primary channel: {channel}\n"
                "- Social presence: {Q31}\n\n"
                "Produce:\n"
                "1. **Retargeting budget** (specific monthly amount)\n"
                "2. **Platform recommendation** with rationale\n"
                "3. **Budget per audience tier**\n"
                "4. **Frequency caps** per tier\n"
                "5. **Setup checklist** (step-by-step, matched to their tech level)\n"
                "6. **Expected metrics**: impressions, clicks, conversions, ROAS for retargeting\n\n"
                "If {Q44} < $1,500/mo: explicitly recommend skipping retargeting "
                "and allocating 100% to prospecting."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "All ad copy must be complete. "
                "Audience definitions must be specific enough to configure in an ad platform."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/fc5_retargeting_creative.html",
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate JSON for retargeting creative mockups per audience segment.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "creatives": [\n'
                '    {"audience_tier": "hot", "format": "static", '
                '     "headline": "...", "body": "...", "cta": "...", '
                '     "visual_description": "..."},\n'
                '    {"audience_tier": "warm", "format": "carousel", '
                '     "headline": "...", "body": "...", "cta": "...", '
                '     "visual_description": "..."}\n'
                "  ]\n"
                "}\n"
                "```\n"
                "Include one creative per audience tier (3-4 total)."
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q10", "Q22", "Q28", "Q30", "Q31",
        "Q33", "Q44",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5, DocID.U6],
    downstream_consumers=[DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Skip if budget < $1,500. Revisit when traffic builds.",
        Maturity.GROWING: "Basic retargeting (Tier 1 + Tier 2). Single platform.",
        Maturity.ESTABLISHED: "Full tiered retargeting. Multi-platform. Dynamic creatives.",
        Maturity.PIVOT: "New pixel on new site. Start collecting data before launching retargeting.",
    },
    bottleneck_adaptations={
        Bottleneck.CONVERSION: "THIS IS HIGH-LEVERAGE. Retargeting converts warm visitors who left.",
        Bottleneck.VISIBILITY: "Standard depth — retargeting needs existing traffic.",
        Bottleneck.LEAD_GENERATION: "Retarget LP visitors who didn't convert with lead magnet offers.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Retarget past customers with upsell/cross-sell (hot audience variant).",
        Bottleneck.WRONG_CLIENTS: "Exclusion rules are the priority — don't waste budget on wrong audiences.",
    },
    quality_rules=[
        "Audience definitions must be specific enough to configure in Meta/Google Ads.",
        "Exclusion rules are mandatory — never retarget existing customers with acquisition ads.",
        "Frequency caps must be set — overexposure kills brand perception.",
        "Creative copy must differ by audience tier — don't show urgency ads to cold visitors.",
        "Budget recommendation must be realistic — if they can't afford retargeting, say so.",
        "If total traffic < 500 visits/mo: explicitly recommend waiting before launching retargeting.",
    ],
)