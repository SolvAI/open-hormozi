# CH2 - Social Ads Strategy spec
"""CH2: Social Ads Strategy.

Paid social acquisition: platform selection, audience targeting,
creative briefs, campaign structure, and budget planning.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH2_SPEC = DocSpec(
    id=DocID.CH2,
    name="Social Ads Strategy",
    tier=Tier.CHANNEL,
    purpose=(
        "Design paid social media campaigns: platform selection with rationale, "
        "audience targeting, creative briefs for multiple formats, campaign structure, "
        "budget allocation, and a creative testing plan."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Platform Selection & Rationale",
            purpose="Pick 1-2 platforms and explain exactly why",
            tone_note="Decisive. Don't say 'all platforms have merits.' Pick and commit.",
            static_content=(
                "## Platform Decision Matrix\n\n"
                "| Platform | Best Audience | Ad Formats | Min Budget | Strength |\n"
                "|----------|-------------|-----------|-----------|----------|\n"
                "| **Meta (FB+IG)** | B2C broad, local, 25-55 | Image, video, carousel, stories | $500/mo | Targeting depth, retargeting |\n"
                "| **Instagram** | Visual, lifestyle, 18-40 | Stories, reels, feed | Via Meta | Visual storytelling |\n"
                "| **LinkedIn** | B2B, professionals, decision-makers | Sponsored posts, InMail, docs | $1,000/mo | Professional targeting |\n"
                "| **TikTok** | Gen Z, discovery, viral potential | Short video, spark ads | $500/mo | Organic reach boost |\n"
                "| **Pinterest** | DIY, décor, fashion, wedding, food | Pins, idea pins | $300/mo | High purchase intent |\n\n"
                "### The Rule: Max 2 Platforms\n"
                "Under $3k/mo: ONE platform. Each platform requires different creative, "
                "different copy, different optimization. Splitting thin = losing everywhere."
            ),
            dynamic_prompt=(
                "Select the platform(s) for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Product/service: {Q7}, {Q8}\n"
                "- Target customer: {Q34}\n"
                "- Customer location: {Q5}\n"
                "- Budget: {Q44}\n"
                "- Existing social presence: {Q31}\n\n"
                "Produce:\n"
                "1. **Primary platform** with 3 specific reasons\n"
                "2. **Why NOT the other platforms** (1 sentence each)\n"
                "3. **If budget > $2k/mo**: recommended secondary platform\n\n"
                "If local business: Meta (FB+IG) with radius targeting is almost always the answer.\n"
                "If B2B: LinkedIn if deal size justifies the higher CPC.\n"
                "If visual product: Instagram/Pinterest depending on audience age."
            ),
        ),
        SectionSpec(
            name="Audience Targeting",
            purpose="Define precise audiences for prospecting and retargeting",
            tone_note="Specific. Not 'women 25-45 interested in fashion' — that's millions of people.",
            static_content=(
                "## Audience Architecture\n\n"
                "### Three Audience Types\n"
                "| Type | What | Use |\n"
                "|------|------|-----|\n"
                "| **Cold** (Prospecting) | Interest/behavior/lookalike targeting | New customer acquisition |\n"
                "| **Warm** (Retargeting) | Website visitors, video viewers, engagers | Conversion of known interest |\n"
                "| **Hot** (Custom) | Email list, past buyers | Upsell, loyalty, lookalike seed |\n\n"
                "### Targeting Layers (Meta/LinkedIn)\n"
                "1. **Demographics**: age, gender, location, language\n"
                "2. **Interests**: pages liked, content engaged with\n"
                "3. **Behaviors**: purchase history, device usage, travel\n"
                "4. **Lookalike**: 1% lookalike of your best customers (most powerful)\n"
                "5. **Custom**: from your data (email list, pixel data)\n\n"
                "### The Targeting Paradox\n"
                "Too broad = wasted spend. Too narrow = no reach. "
                "Sweet spot: 100k-500k for local, 500k-2M for national."
            ),
            dynamic_prompt=(
                "Build the audience strategy for this client.\n\n"
                "Based on:\n"
                "- ICP from U2 (upstream)\n"
                "- Customer location: {Q5}\n"
                "- Physical location: {Q6}\n"
                "- B2B/B2C: {Q38}\n"
                "- Existing assets: {Q30} (email list), {Q31} (social)\n\n"
                "Define:\n"
                "1. **Cold audience 1**: interest-based targeting (specific interests to select)\n"
                "2. **Cold audience 2**: lookalike (from what seed, what %)\n"
                "3. **Warm audience**: retargeting definition (who, what window)\n"
                "4. **Exclusions**: who to exclude from each audience\n"
                "5. **Estimated audience size** per audience\n\n"
                "If local ({Q5}=local): radius targeting + interest layering.\n"
                "If no email list ({Q30}=no): skip custom audiences, focus cold + pixel retargeting."
            ),
        ),
        SectionSpec(
            name="Creative Briefs",
            purpose="Specify what ads to create — format, message, visual direction",
            tone_note="These are briefs, not finished ads. But specific enough to execute.",
            static_content=(
                "## Creative Format Priority\n\n"
                "| Format | Engagement | Production | Best For |\n"
                "|--------|-----------|-----------|----------|\n"
                "| **Static image** | Medium | Low | Product showcase, testimonials |\n"
                "| **Carousel** | High | Medium | Multiple products, step-by-step |\n"
                "| **Short video (15-30s)** | Highest | Medium-High | Storytelling, demos, UGC |\n"
                "| **UGC-style** | Very High | Low-Medium | Authenticity, social proof |\n"
                "| **Story/Reel** | High | Medium | Full-screen, immersive |\n\n"
                "### The Testing Framework\n"
                "Test in this order:\n"
                "1. **Angles** first (pain vs outcome vs proof — which resonates?)\n"
                "2. **Formats** second (static vs video vs carousel)\n"
                "3. **Copy** third (headline variations)\n"
                "4. **Visuals** last (different images/videos)\n\n"
                "Never test everything at once. One variable at a time."
            ),
            dynamic_prompt=(
                "Create 4-6 creative briefs for this client.\n\n"
                "Using messaging angles from U5 (upstream), produce:\n"
                "For each creative:\n"
                "1. **Format**: static / carousel / video / UGC\n"
                "2. **Placement**: feed / stories / reels\n"
                "3. **Angle**: which U5 messaging angle\n"
                "4. **Visual direction**: what the image/video shows (specific)\n"
                "5. **Primary text** (ad copy — full text)\n"
                "6. **Headline** (short, appears below image on feed)\n"
                "7. **CTA button**: Shop Now / Learn More / Book Now / etc.\n\n"
                "Include at least:\n"
                "- 1 pain-focused creative\n"
                "- 1 proof/testimonial creative (from {Q33})\n"
                "- 1 offer-focused creative\n"
                "- 1 video concept (even if they'll need to produce it)\n\n"
                "Write all copy in English."
            ),
        ),
        SectionSpec(
            name="Campaign Structure & Budget",
            purpose="Organize campaigns for clean testing and optimization",
            tone_note="Structure enables learning. Bad structure means data you can't read.",
            static_content=(
                "## Campaign Structure\n\n"
                "```\n"
                "Account\n"
                "├── Campaign: Prospecting (Cold)\n"
                "│   ├── Ad Set: Interest Audience A\n"
                "│   ├── Ad Set: Interest Audience B\n"
                "│   └── Ad Set: Lookalike 1%\n"
                "├── Campaign: Retargeting (Warm)\n"
                "│   ├── Ad Set: Website visitors 7d\n"
                "│   └── Ad Set: Video viewers 50%+\n"
                "└── Campaign: Testing\n"
                "    └── Ad Set: Broad (for creative testing)\n"
                "```\n\n"
                "### Budget Split Rule\n"
                "- **70-80%** → Prospecting (cold)\n"
                "- **10-20%** → Retargeting (warm)\n"
                "- **10%** → Testing (new creatives/audiences)\n\n"
                "### Daily Budget Minimums\n"
                "- Per ad set: $10-15/day minimum (below this, algorithm can't optimize)\n"
                "- If total budget < $30/day: run ONE ad set, not three"
            ),
            dynamic_prompt=(
                "Design the campaign structure and budget for this client.\n\n"
                "Budget: {Q44}\n"
                "Platform: from selection above\n\n"
                "Produce:\n"
                "1. **Campaign map** with ad sets and targeting per set\n"
                "2. **Budget allocation** (daily amounts per campaign)\n"
                "3. **Creative assignment**: which creative brief goes in which ad set\n"
                "4. **Week 1-4 testing plan**: what to test in which order\n"
                "5. **Expected metrics**: impressions, clicks, leads, cost per lead\n\n"
                "If budget < $1,000/mo: ONE prospecting campaign, no retargeting yet. "
                "State this constraint explicitly."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment="All ad copy must be complete and ready to use.",
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/ch2_creative_mockup.html",
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate JSON for social ad creative mockups.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "mockups": [\n'
                '    {"platform": "instagram_feed", "headline": "...", '
                '     "primary_text": "...", "cta": "...", '
                '     "visual_description": "Description of the image/video"}\n'
                "  ]\n"
                "}\n"
                "```\n"
                "Include 3 mockups: 1 feed, 1 story, 1 carousel."
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q5", "Q6", "Q7", "Q8",
        "Q10", "Q22", "Q30", "Q31", "Q33", "Q34",
        "Q38", "Q40", "Q44",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U7, DocID.U8, DocID.FC1, DocID.FC5],
    maturity_adaptations={
        Maturity.STARTER: "Start with 1 campaign, 2-3 creatives. Emphasis on learning, not scaling.",
        Maturity.GROWING: "Full prospecting + retargeting structure. Creative testing plan.",
        Maturity.ESTABLISHED: "Advanced: lookalike audiences from CRM, dynamic creative, catalog ads.",
        Maturity.PIVOT: "New audience, new creatives. Test angles fast.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Maximum prospecting budget. Broad-ish targeting to build awareness.",
        Bottleneck.LEAD_GENERATION: "Tighter targeting. Lead-gen objective. Strong LP (FC1).",
        Bottleneck.CONVERSION: "Retargeting is the priority. Warm audiences + proof creatives.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Use ads for re-engagement of past customers (hot audiences).",
        Bottleneck.WRONG_CLIENTS: "Narrow targeting. Exclusions are as important as inclusions.",
    },
    quality_rules=[
        "Platform recommendation must be ONE platform (two only if budget > $2k/mo).",
        "All ad copy must be complete — no 'write something about your product here.'",
        "Audience sizes must be estimated (order of magnitude).",
        "Budget split must add up to 100% and not exceed stated budget.",
        "Creative briefs must be specific enough for a designer to execute.",
        "Testing plan must specify ONE variable at a time — never test 3 things simultaneously.",
    ],
)