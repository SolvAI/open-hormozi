"""U2: Avatar & Ideal Customer Profile.

Builds the dream customer profile that shapes messaging, channel targeting,
offer design, and content strategy across all downstream documents.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U2_SPEC = DocSpec(
    id=DocID.U2,
    name="Avatar & ICP",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Define the dream customer with enough specificity to drive targeting, "
        "messaging, and offer design. For B2B: company profile + buyer persona. "
        "For B2C: customer archetype. For local: neighborhood/radius profile."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Demographics & Firmographics",
            purpose="Hard facts about who the customer IS (measurable, targetable attributes)",
            tone_note="B2B: firmographics first (company size, revenue, industry). B2C: demographics. Local: neighborhood profile.",
            static_content=(
                "## Why Demographics Matter (and Where They Don't)\n\n"
                "Demographics tell you WHERE to find someone. Psychographics tell you HOW to persuade them.\n"
                "You need both, but most businesses over-invest in demographics and under-invest in psychographics.\n\n"
                "### B2B: Firmographic Profile\n"
                "- Company size (employees, revenue)\n"
                "- Industry / vertical\n"
                "- Growth stage (startup, scaling, mature)\n"
                "- Tech stack / sophistication level\n"
                "- Geographic scope\n\n"
                "### B2C: Demographic Profile\n"
                "- Age range, gender (if relevant), location\n"
                "- Income bracket, education level\n"
                "- Life stage (student, young professional, parent, retiree)\n"
                "- Digital behavior (platforms, consumption habits)\n\n"
                "### Local: Radius Profile\n"
                "- Distance from location (walking, driving, transit)\n"
                "- Neighborhood characteristics\n"
                "- Foot traffic patterns (lunch rush, evening, weekend)\n"
                "- Competitor proximity"
            ),
            dynamic_prompt=(
                "Build the demographic/firmographic profile from:\n"
                "- Client's description of ideal customer: {Q34}\n"
                "- Business type: {Q1}\n"
                "- Customer geography: {Q5}\n"
                "- B2B company size: {Q38}\n"
                "- B2B buyer role: {Q39}\n"
                "- Physical location: {Q6}\n\n"
                "If B2B: build both the COMPANY profile (who to target on LinkedIn/Apollo) "
                "and the BUYER profile (who you actually talk to). They're different.\n"
                "If local: include radius-specific details. A restaurant's ICP at lunch ≠ dinner.\n"
                "Be specific enough that someone could use this to build a LinkedIn Sales Nav filter "
                "or a Meta Ads audience."
            ),
        ),
        SectionSpec(
            name="Psychographics & Buying Triggers",
            purpose="Internal motivations, fears, desires, and what triggers the buying moment",
            tone_note="This is where the real insight lives. Go deep. In English.",
            static_content=(
                "## The Psychographic Layer\n\n"
                "People buy for emotional reasons and justify with logic.\n\n"
                "### The 5 Core Pain Points\n"
                "Every ICP has 3-5 pains that are so acute they'd pay to make them stop. "
                "These aren't mild annoyances — they're the things that keep them up at night, "
                "make them vent to colleagues, or trigger an angry Google search.\n\n"
                "### The 5 Desired Outcomes\n"
                "The mirror of pains. Not 'absence of problem' but a vivid picture of life AFTER. "
                "Use their words, not yours.\n\n"
                "### Buying Triggers\n"
                "What events FORCE them to act? Not 'they want to improve' but "
                "'their CTO quit and they have a release in 6 weeks' or "
                "'they got a bad health report and their doctor said lose 20kg.' "
                "Triggers are external events that create urgency.\n\n"
                "### Decision-Making Process\n"
                "- Who influences the decision?\n"
                "- What do they research before buying?\n"
                "- What objections arise? (captured in their own internal dialogue)\n"
                "- How long from trigger to purchase?"
            ),
            dynamic_prompt=(
                "Build the psychographic profile from:\n"
                "- Problem solved: {Q35}\n"
                "- Consequences of inaction: {Q36}\n"
                "- Current alternatives: {Q37}\n"
                "- Ideal customer description: {Q34}\n"
                "- Decision maker: {Q17} (if B2B with consultative sale)\n"
                "- Sales cycle length: {Q16}\n\n"
                "Produce:\n"
                "1. **5 Core Pains** — specific, in the customer's voice, "
                "not the client's professional jargon\n"
                "2. **5 Desired Outcomes** — vivid, emotional, specific\n"
                "3. **3-5 Buying Triggers** — external events that force action\n"
                "4. **Decision-Making Process** — who's involved, what they research, "
                "timeline from trigger to purchase\n\n"
                "Use the actual vocabulary from Q34-Q37."
            ),
        ),
        SectionSpec(
            name="Where They Hang Out",
            purpose="Map where this audience spends time (online + offline) for targeting",
            tone_note="Practical. This directly feeds CH1-CH7 targeting decisions.",
            static_content=(
                "## Finding Your Audience\n\n"
                "### Online Presence\n"
                "- Which platforms (LinkedIn, Instagram, YouTube, forums, Reddit, Slack communities)?\n"
                "- What do they search for on Google? (intent keywords)\n"
                "- Which newsletters, podcasts, or influencers do they follow?\n"
                "- What Facebook/LinkedIn groups are they in?\n\n"
                "### Offline Presence\n"
                "- Which events, conferences, meetups?\n"
                "- Which professional associations?\n"
                "- Physical locations (coworking spaces, gyms, specific neighborhoods)?\n"
                "- Referral networks (who do they already trust?)\n\n"
                "### The 'Watering Hole' Principle\n"
                "Don't go where everyone is. Go where YOUR audience gathers "
                "in concentrated numbers. A niche LinkedIn group of 2,000 people "
                "beats Instagram's 2 billion users."
            ),
            dynamic_prompt=(
                "Map this specific audience's watering holes based on:\n"
                "- Business type: {Q1}\n"
                "- Customer geography: {Q5}\n"
                "- Industry: {Q2}\n"
                "- B2B company size: {Q38}\n"
                "- B2B buyer role: {Q39}\n"
                "- Customer description: {Q34}\n\n"
                "Be SPECIFIC: not 'they're on LinkedIn' but 'CTOs of French tech startups "
                "(10-50 employees) active in groups like [X], following influencers like [Y], "
                "attending events like [Z].'\n\n"
                "This section directly supports the channel strategy. "
                "If primary channel is {channel}, emphasize the watering holes "
                "accessible through that channel."
            ),
        ),
        SectionSpec(
            name="Before & After Transformation Grid",
            purpose="Visualize the complete transformation the client delivers",
            tone_note="Powerful. This becomes copy fuel for FC1, U5, BM1, and ads.",
            static_content=(
                "## The Transformation Grid\n\n"
                "Every purchase is a transformation from a BEFORE state to an AFTER state. "
                "Map it across 4 dimensions:\n\n"
                "| Dimension | BEFORE (pain state) | AFTER (dream state) |\n"
                "|-----------|--------------------|--------------------||\n"
                "| **Have** (tangible) | What they have/don't have | What they'll have |\n"
                "| **Feel** (emotional) | How they feel | How they'll feel |\n"
                "| **Status** (social) | How others see them | How others will see them |\n"
                "| **Day-to-Day** (practical) | What their typical day looks like | What it will look like |\n\n"
                "Write these in FIRST PERSON — as the customer would describe it. "
                "'I'm spending 3 hours a day on…' not 'The client currently allocates…'"
            ),
            dynamic_prompt=(
                "Build the transformation grid for this client's customer.\n\n"
                "BEFORE state derived from: {Q35} (problem), {Q36} (consequences), {Q37} (current alternatives)\n"
                "AFTER state derived from: {Q7} (what client delivers), {Q34} (ideal customer situation)\n\n"
                "Write in FIRST PERSON from the customer's perspective.\n"
                "Use their vocabulary, not the client's professional jargon.\n\n"
                "4 rows × 2 columns. Each cell should be 2-3 sentences — vivid, specific, emotional.\n"
                "This grid gets reused verbatim in landing pages (FC1), "
                "sales scripts (BM1), and ad copy (CH1/CH2)."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Use <h2> for major sections, <h3> for subsections. "
                "Format the transformation grid as an HTML <table>. "
                "Use <ul> for pains, outcomes, and trigger lists."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/u2_persona_card.html",
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate JSON content for a persona card visual.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "persona_name": "Fictional first name representing the archetype",\n'
                '  "persona_title": "Role / description (e.g., CTO de startup SaaS, 35 ans)",\n'
                '  "key_quote": "One sentence in their voice that captures their main pain",\n'
                '  "demographics": ["Age: 30-45", "Location: ...", "Revenue: ..."],\n'
                '  "top_pains": ["Pain 1", "Pain 2", "Pain 3"],\n'
                '  "desired_outcomes": ["Outcome 1", "Outcome 2", "Outcome 3"],\n'
                '  "buying_triggers": ["Trigger 1", "Trigger 2"],\n'
                '  "channels": ["Where they hang out 1", "Where they hang out 2"]\n'
                "}\n"
                "```"
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q5", "Q6", "Q7",
        "Q10", "Q16", "Q17",
        "Q34", "Q35", "Q36", "Q37", "Q38", "Q39",
    ],
    upstream_deps=[DocID.U1],
    downstream_consumers=[
        DocID.U3, DocID.U5, DocID.U6,
        DocID.BM1, DocID.BM5,
        DocID.CH1, DocID.CH2, DocID.CH3,
        DocID.FC1, DocID.FC3,
    ],
    maturity_adaptations={
        Maturity.STARTER: (
            "The client may not know their ICP well yet. Help them DISCOVER it "
            "from the clues in their answers. Frame as 'hypothesis to validate' not 'truth.'"
        ),
        Maturity.GROWING: (
            "Client has some clients — use patterns from their actual experience. "
            "Ask: 'who were your best 3 clients? What do they have in common?'"
        ),
        Maturity.ESTABLISHED: (
            "Refine and sharpen an existing understanding. Focus on the most PROFITABLE "
            "segment, not just the most common. May need to exclude low-value customer types."
        ),
        Maturity.PIVOT: (
            "Bridge: the customer they served before may overlap with who they serve now. "
            "Map transferable knowledge about buyer psychology."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Emphasize WHERE they hang out — this feeds directly into channel targeting.",
        Bottleneck.LEAD_GENERATION: "Emphasize buying triggers — what makes them raise their hand.",
        Bottleneck.CONVERSION: "Emphasize objections and decision-making process — what stops them from buying.",
        Bottleneck.PRICING: "Emphasize perceived value and what they currently pay for alternatives.",
        Bottleneck.RETENTION: "Emphasize what makes them STAY vs leave — loyalty drivers.",
        Bottleneck.WRONG_CLIENTS: (
            "THIS IS THE PRIORITY. Build the IDEAL avatar sharply, then explicitly describe "
            "the ANTI-avatar (who to repel). The positioning and offer must filter."
        ),
    },
    quality_rules=[
        "Pains and outcomes must be in the CUSTOMER'S voice, not the client's professional jargon.",
        "If B2B: always distinguish company profile from buyer persona. The company doesn't buy — the person does.",
        "If local: include radius-specific details (lunch crowd vs dinner crowd, walking distance vs driving).",
        "Buying triggers must be EVENTS, not desires. 'Wants to grow' is not a trigger. 'Lost their biggest client' is.",
        "The transformation grid must make the reader feel the emotional gap between before and after.",
        "Everything in this document gets reused downstream — accuracy here compounds, errors here compound too.",
        "Don't invent demographics the client didn't provide. If Q38/Q39 are N/A, don't fabricate B2B data.",
    ],
)