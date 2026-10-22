"""CH4: Organic Content Strategy.

Content-led growth: platform selection, pillars, frameworks,
cadence, repurposing, and a 90-day calendar.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH4_SPEC = DocSpec(
    id=DocID.CH4,
    name="Organic Content Strategy",
    tier=Tier.CHANNEL,
    purpose=(
        "Build a sustainable organic content engine: platform selection, "
        "3-4 content pillars, repeatable frameworks, posting cadence, "
        "repurposing flow, and a 90-day content calendar."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Platform & Format Selection",
            purpose="Pick the platform and formats that match their strengths and audience",
            tone_note="Honest about what each platform demands. Don't recommend video to someone who hates camera.",
            static_content=(
                "## Platform Selection Matrix\n\n"
                "| Platform | Content Type | Posting Freq | Time Investment | Best For |\n"
                "|----------|-------------|-------------|----------------|----------|\n"
                "| **LinkedIn** | Text posts, articles, docs | 3-5x/week | 3-5 hrs/week | B2B, expertise, networking |\n"
                "| **Instagram** | Reels, carousels, stories | 4-7x/week | 5-8 hrs/week | Visual, lifestyle, local |\n"
                "| **YouTube** | Long-form video | 1-2x/week | 8-15 hrs/week | Education, tutorials, authority |\n"
                "| **TikTok** | Short video | 5-7x/week | 4-8 hrs/week | Discovery, younger audience |\n"
                "| **X/Twitter** | Short text, threads | 5-10x/week | 2-4 hrs/week | Tech, media, hot takes |\n"
                "| **Newsletter** | Long-form email | 1x/week | 2-4 hrs/week | Owned audience, depth |\n"
                "| **Blog/SEO** | Articles | 1-2x/month | 4-8 hrs/month | Long-term search traffic |\n\n"
                "### The Honest Assessment\n"
                "- If you won't show your face: YouTube/TikTok/Instagram Reels are severely limited\n"
                "- If you hate writing: LinkedIn text posts are painful\n"
                "- If you have 2 hrs/week: pick newsletter OR LinkedIn. Not both.\n"
                "- Video is highest impact but highest effort. Start with what you'll actually DO."
            ),
            dynamic_prompt=(
                "Select the platform and formats for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Target audience: {Q34}\n"
                "- Hard nos: {Q48}\n"
                "- Current presence: {Q31}\n"
                "- Time available: {Q45}\n"
                "- Tech comfort: {Q47}\n\n"
                "Produce:\n"
                "1. **Primary platform** with rationale\n"
                "2. **Top 2 content formats** on that platform\n"
                "3. **What they should NOT do** (based on constraints/hard nos)\n"
                "4. **Realistic time commitment** per week\n\n"
                "If {Q48} includes 'show my face': exclude video-first platforms.\n"
                "If {Q45} < 5 hrs: max 1 platform, 2-3 posts/week."
            ),
        ),
        SectionSpec(
            name="Content Pillars & Frameworks",
            purpose="Define 3-4 repeatable content themes with plug-and-play templates",
            tone_note="Frameworks reduce the 'what do I post?' paralysis. Give them a system, not homework.",
            static_content=(
                "## Content Pillars\n\n"
                "A content pillar is a recurring theme that your audience cares about "
                "and that positions you as an expert.\n\n"
                "### The 4 Pillar Types\n"
                "| Pillar | Purpose | Example |\n"
                "|--------|---------|--------|\n"
                "| **Authority** | Prove expertise | Industry insights, how-tos, frameworks |\n"
                "| **Proof** | Show results | Case studies, before/after, client wins |\n"
                "| **Relatability** | Build connection | Behind-the-scenes, mistakes, personal story |\n"
                "| **Engagement** | Start conversations | Polls, hot takes, questions, memes |\n\n"
                "### Frameworks (Plug-and-Play)\n"
                "| Framework | Structure |\n"
                "|-----------|----------|\n"
                "| **Myth-Buster** | 'Everyone thinks X. Here's why Y.' |\n"
                "| **Step-by-Step** | '3 steps to [outcome]:' |\n"
                "| **Story→Lesson** | 'Last week I [experience]. Here's what I learned:' |\n"
                "| **Hot Take** | 'Unpopular opinion: [controversial but defensible statement]' |\n"
                "| **Before/After** | 'Client came to me with X. 3 months later: Y.' |\n"
                "| **Tool/Tip** | 'The one [tool/hack/trick] that changed my [domain]:' |\n"
                "| **Question** | 'How do you handle [common industry challenge]?' |"
            ),
            dynamic_prompt=(
                "Design the content pillars and frameworks for this client.\n\n"
                "Based on:\n"
                "- What they sell: {Q7}\n"
                "- Expertise: {Q2}\n"
                "- Target audience: {Q34}\n"
                "- Problem solved: {Q35}\n"
                "- Proof available: {Q32}, {Q33}\n\n"
                "Produce:\n"
                "1. **3-4 content pillars** specific to their domain (not the generic 4 above)\n"
                "2. **3 framework templates per pillar** with fill-in-the-blank structure\n"
                "3. **10 specific post ideas** (titles/hooks) distributed across pillars\n"
                "4. **Pillar distribution**: what % of posts per pillar\n\n"
                "Pillar names must be specific: not 'Authority' but 'Technical Deep Dives' "
                "or 'Menu Secrets' or 'Client Transformations'."
            ),
        ),
        SectionSpec(
            name="Repurposing Flow & 90-Day Calendar",
            purpose="Create more content with less effort through systematic repurposing",
            tone_note="The calendar is the deliverable. Make it so specific they can execute on autopilot.",
            static_content=(
                "## The 1→5 Repurposing Rule\n\n"
                "Create ONE substantial piece per week. Repurpose into 4-5 derivative pieces.\n\n"
                "### Example Flow\n"
                "```\n"
                "1 Blog Post / Long Video\n"
                "├── 3 social media posts (key takeaways)\n"
                "├── 1 carousel (step-by-step extracted)\n"
                "├── 1 email newsletter excerpt\n"
                "└── 1 short video clip (if video source)\n"
                "```\n\n"
                "### 90-Day Calendar Structure\n"
                "| Week | Pillar | Anchor Content | Derivative 1 | Derivative 2 | Derivative 3 |\n"
                "Rotate pillars systematically. Never do the same pillar 3 weeks in a row."
            ),
            dynamic_prompt=(
                "Build the 90-day content calendar for this client.\n\n"
                "Using:\n"
                "- Platform: from selection above\n"
                "- Pillars: from pillar design above\n"
                "- Posting cadence: based on {Q45} time available\n\n"
                "Produce:\n"
                "1. **Repurposing flow** specific to their chosen platform and format\n"
                "2. **Week 1-12 calendar** with:\n"
                "   - Week number\n"
                "   - Pillar\n"
                "   - Anchor content idea (specific title/hook)\n"
                "   - 2-3 derivative posts\n"
                "   - Publication dates (day of week)\n"
                "3. **Metrics to track** (not vanity — engagement that leads to business)\n"
                "4. **Growth tactics** specific to the platform (hashtag strategy, "
                "collaboration, commenting strategy, etc.)\n\n"
                "Calendar must have 12 weeks of SPECIFIC ideas, not 'post about [pillar]'."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment="Calendar must have 12 weeks of specific content ideas.",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q7", "Q31", "Q32", "Q33",
        "Q34", "Q35", "Q45", "Q47", "Q48",
    ],
    upstream_deps=[DocID.U2, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Low frequency (2-3x/week). Authority + engagement pillars only. Build the habit.",
        Maturity.GROWING: "Full 4-pillar system. Repurposing flow. Consistency is the lever.",
        Maturity.ESTABLISHED: "Delegate content creation. Focus on thought leadership and authority pillar.",
        Maturity.PIVOT: "Content bridges old authority into new domain. Story→Lesson framework is key.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Maximum posting frequency. Emphasize discovery tactics (hashtags, collabs).",
        Bottleneck.LEAD_GENERATION: "Content must include CTAs. Authority content → lead magnet funnel.",
        Bottleneck.CONVERSION: "Proof pillar is priority. Case studies, testimonials, results.",
        Bottleneck.PRICING: "Authority content justifies premium. Position as the expert.",
        Bottleneck.RETENTION: "Content keeps existing clients engaged and referring.",
        Bottleneck.WRONG_CLIENTS: "Content must speak to the RIGHT audience. Identity-first framing.",
    },
    quality_rules=[
        "Content calendar must have 12 weeks of SPECIFIC ideas — not vague pillar assignments.",
        "Framework templates must be fill-in-the-blank usable. Not 'write about your expertise.'",
        "Platform recommendation must respect hard nos (Q48). Never recommend video to someone who refuses camera.",
        "Time estimates must be honest. Don't claim '3 posts/week in 1 hour.'",
        "Metrics section must distinguish vanity metrics from business metrics.",
        "All post ideas must be in English.",
    ],
)