"""U5: Positioning & Messaging.

Defines how the client differentiates from every alternative and
provides the messaging toolkit used across all touchpoints.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U5_SPEC = DocSpec(
    id=DocID.U5,
    name="Positioning & Messaging",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Define the client's core differentiation, competitive positioning, "
        "and provide a complete messaging toolkit (angles, headlines, vocabulary) "
        "that ensures consistency across all channels and touchpoints."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Core Differentiation Statement",
            purpose="One sentence that captures why THIS business, not any alternative",
            tone_note="STARTER: help them find it. ESTABLISHED: sharpen what exists. PIVOT: bridge old authority to new domain.",
            static_content=(
                "## The Differentiation Test\n\n"
                "Your positioning statement must pass 3 tests:\n\n"
                "1. **Specificity Test**: Could a competitor say the exact same thing? "
                "If yes, it's not differentiation — it's a category description.\n"
                "2. **So-What Test**: Does the customer care? 'We use agile methodology' "
                "fails. 'You get a working prototype in 2 weeks, not 2 months' passes.\n"
                "3. **Proof Test**: Can you back it up? Bold claims without proof are just noise.\n\n"
                "### The Positioning Formula\n"
                "```\n"
                "For [ideal customer] who [situation/trigger],\n"
                "[your business] is the [category/frame]\n"
                "that [key differentiator]\n"
                "unlike [primary alternative] which [alternative's limitation].\n"
                "We prove it by [proof mechanism].\n"
                "```\n\n"
                "### Common Positioning Axes\n"
                "- **Specialization**: 'We only do X for Y' (niche focus)\n"
                "- **Process**: 'Our method delivers Z in half the time' (how you do it)\n"
                "- **Outcome guarantee**: 'X result or your money back' (risk reversal)\n"
                "- **Experience premium**: 'We've done this 500 times for companies like yours' (proof)\n"
                "- **Access**: 'Direct line to senior experts, not junior staff' (quality of engagement)"
            ),
            dynamic_prompt=(
                "Craft the core differentiation statement using the formula.\n\n"
                "Inputs:\n"
                "- What they sell: {Q7}\n"
                "- Ideal customer: {Q34}\n"
                "- Problem solved: {Q35}\n"
                "- Current alternatives: {Q37}\n"
                "- Proof available: {Q32}, {Q33}\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Operating years: {Q3}\n\n"
                "Produce:\n"
                "1. The filled positioning formula (complete sentence)\n"
                "2. The positioning AXIS chosen (specialization, process, outcome, experience, or access) "
                "with rationale for why this axis is strongest for THIS client\n"
                "3. Two alternative positioning options they could test later\n\n"
                "If {Q1} = local business: positioning should reference geography and local relevance.\n"
                "If {Q1} = freelance consultant: positioning should separate them from the "
                "commodity marketplace crowd. What makes them worth 3× the average?"
            ),
        ),
        SectionSpec(
            name="Competitive Alternatives Matrix",
            purpose="Map every alternative and show where the client wins",
            tone_note="Honest. Acknowledge where alternatives are better on some axes — then reframe.",
            static_content=(
                "## The 4 Alternatives Every Buyer Considers\n\n"
                "Your competition is NOT just other businesses like yours. "
                "Every buyer evaluates 4 alternatives:\n\n"
                "1. **Direct competitors**: Other businesses offering similar solutions\n"
                "2. **Indirect competitors**: Different solutions to the same problem "
                "(e.g., hiring in-house vs. hiring a freelancer)\n"
                "3. **DIY**: Doing it themselves (tutorials, templates, tools)\n"
                "4. **Do nothing**: Living with the problem (inertia — your biggest competitor)\n\n"
                "### The Comparison Matrix\n"
                "| Criteria | You | Competitor A | DIY | Do Nothing |\n"
                "|----------|-----|-------------|-----|------------|\n"
                "| Speed to result | | | | |\n"
                "| Cost (total, not just price) | | | | |\n"
                "| Risk of failure | | | | |\n"
                "| Effort required from buyer | | | | |\n"
                "| Proof / track record | | | | |\n\n"
                "Win on at least 3 of 5. For the 1-2 where you lose, REFRAME:\n"
                "'Yes, DIY is cheaper upfront — but factor in 6 months of your time at $X/hour...'"
            ),
            dynamic_prompt=(
                "Build the competitive alternatives matrix for this client.\n\n"
                "From {Q37}: what alternatives the buyer currently considers.\n"
                "From {Q7}, {Q10}, {Q35}: what the client offers and at what price.\n"
                "From U3 upstream: the value stack and guarantee.\n\n"
                "Identify:\n"
                "1. **2-3 direct competitors** (based on industry {Q2} and offer type {Q8})\n"
                "2. **The DIY alternative** (what would the buyer do themselves?)\n"
                "3. **Do nothing** (what happens if they stay with status quo? from {Q36})\n\n"
                "Fill the 5-criteria comparison matrix with honest assessments.\n"
                "For each criterion where the client LOSES, write the reframe argument.\n\n"
                "Adapt competitor examples to the client's business type and market."
            ),
        ),
        SectionSpec(
            name="Messaging Angles",
            purpose="3 ranked messaging approaches to test across touchpoints",
            tone_note="Practical. These become ad copy angles, email subject lines, LP headlines.",
            static_content=(
                "## What Is a Messaging Angle?\n\n"
                "A messaging angle is a lens through which you present the same offer. "
                "Different angles resonate with different segments or at different funnel stages.\n\n"
                "### Common Angle Types\n"
                "- **Pain-first**: Lead with the problem ('Tired of losing clients to...')\n"
                "- **Outcome-first**: Lead with the result ('Get 5 qualified leads per week')\n"
                "- **Proof-first**: Lead with credibility ('Used by 200+ companies including...')\n"
                "- **Process-first**: Lead with how it works ('In 3 steps, we...')\n"
                "- **Enemy-first**: Lead with what you're against ('Unlike agencies that...')\n"
                "- **Identity-first**: Lead with who it's for ('Built for CTOs who...')\n\n"
                "### How to Rank Angles\n"
                "1. If you have strong proof → proof-first\n"
                "2. If the pain is acute and well-known → pain-first\n"
                "3. If the audience is sophisticated → process-first or enemy-first\n"
                "4. If the audience is broad → outcome-first\n"
                "5. If niche positioning → identity-first"
            ),
            dynamic_prompt=(
                "Design 3 ranked messaging angles for this client.\n\n"
                "Inputs:\n"
                "- Problem: {Q35}\n"
                "- Consequences: {Q36}\n"
                "- Ideal customer: {Q34}\n"
                "- Proof level: {Q32}\n"
                "- Alternatives: {Q37}\n"
                "- Offer: {Q7}\n\n"
                "For each angle:\n"
                "1. Name it (Pain-first, Outcome-first, etc.)\n"
                "2. Explain why it fits this client\n"
                "3. Write 3 example headlines using this angle\n"
                "4. Indicate where to use it (ads, LP hero, email subjects, social posts)\n\n"
                "Rank by likely effectiveness for this specific business. "
                "If {Q32} = strong proof: proof-first should rank high. "
                "If {Q32} = none: proof-first is off the table — go pain or outcome."
            ),
        ),
        SectionSpec(
            name="Headline Formulas & Vocabulary",
            purpose="Ready-to-use copy elements for all downstream documents",
            tone_note="A copywriter's toolkit, not theory. Everything here should be copy-paste ready.",
            static_content=(
                "## Headline Formulas\n\n"
                "### The 7 Proven Structures\n"
                "1. **How to [outcome] without [pain]**: 'How to get 5 leads/week without cold calling'\n"
                "2. **[Number] ways to [outcome]**: '3 ways to reduce your hosting costs by 60%'\n"
                "3. **The [adjective] guide to [outcome]**: 'The no-BS guide to pricing your services'\n"
                "4. **Why [surprising truth]**: 'Why your beautiful website is killing your conversions'\n"
                "5. **[Outcome] in [timeframe]**: 'A working MVP in 6 weeks'\n"
                "6. **For [avatar] who [situation]**: 'For CTOs tired of managing freelancers'\n"
                "7. **Stop [mistake] — Start [solution]**: 'Stop quoting hourly — start selling outcomes'\n\n"
                "### Vocabulary Rules\n"
                "Use the customer's language, not industry jargon.\n"
                "Short sentences. Active voice. Concrete nouns over abstract concepts.\n"
                "Numbers beat adjectives. Specifics beat generalities."
            ),
            dynamic_prompt=(
                "Generate the complete vocabulary toolkit for this client.\n\n"
                "1. **10 headlines** using the 7 formulas above, tailored to {Q7}, {Q35}, {Q34}\n"
                "2. **Power words TO USE**: 10-15 words that resonate with this audience\n"
                "3. **Words TO AVOID**: 10-15 words that are jargon, vague, or off-brand\n"
                "4. **Brand voice description**: 3-sentence description of how this business should sound "
                "(formal/informal, expert/accessible, bold/measured)\n\n"
                "All headlines and vocabulary in English."
            ),
        ),
        SectionSpec(
            name="Origin Story Framework",
            purpose="Give the client a narrative structure for their 'why' story",
            tone_note="STARTER: this is their first time articulating it. ESTABLISHED: refine an existing narrative.",
            static_content=(
                "## The Origin Story Structure\n\n"
                "Every strong brand has a story. Not a biography — a transformation narrative:\n\n"
                "```\n"
                "1. WHO I WAS — before this business (relatable starting point)\n"
                "2. THE PROBLEM I SAW — what frustrated/angered/motivated me\n"
                "3. THE TURNING POINT — the specific moment I decided to act\n"
                "4. WHAT I BUILT — the solution (your business/offer)\n"
                "5. WHO I SERVE — the people I care about helping\n"
                "6. THE PROOF — results that validate the journey\n"
                "```\n\n"
                "### Rules\n"
                "- Keep it under 200 words (for a bio) or 60 seconds (for video)\n"
                "- The customer is the hero, not you. Your story exists to build trust.\n"
                "- Vulnerability > perfection. 'I failed at X before figuring out Y' wins.\n"
                "- End with the customer's outcome, not your credentials."
            ),
            dynamic_prompt=(
                "Build an origin story framework from:\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Operating years: {Q3}\n"
                "- What they sell: {Q7}\n"
                "- Problem they solve: {Q35}\n"
                "- Additional context: {Q49}\n\n"
                "Produce:\n"
                "1. A structured origin story outline (6 points filled in with available info)\n"
                "2. A SHORT VERSION (3 sentences — for social media bios, email signatures)\n"
                "3. A MEDIUM VERSION (1 paragraph — for About page, LinkedIn summary)\n\n"
                "If the client provided little personal info: "
                "provide the STRUCTURE with prompting questions they should fill in. "
                "Don't invent a backstory — give them the scaffold."
            ),
        ),
        SectionSpec(
            name="Tone & Style Guidelines",
            purpose="Ensure consistent voice across all 14-21 documents and future content",
            tone_note="Meta — this section defines the tone for everything else.",
            static_content=None,  # Fully dynamic based on business type
            dynamic_prompt=(
                "Define the tone and style guidelines for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1} (a plumber sounds different than a SaaS founder)\n"
                "- Target audience: {Q34}\n"
                "- Maturity: {maturity}\n"
                "- Their own writing style (from Q7, Q35, Q49 — how do THEY naturally write?)\n\n"
                "Produce:\n"
                "1. **Tone spectrum**: where they sit on 4 axes:\n"
                "   - Formal ← → Casual\n"
                "   - Expert ← → Accessible\n"
                "   - Bold ← → Measured\n"
                "   - Warm ← → Direct\n"
                "2. **3 DO examples**: sample sentences in the right voice\n"
                "3. **3 DON'T examples**: same message in the wrong voice\n"
                "4. **Industry-specific note**: what tone is expected/unusual in this vertical?\n\n"
                "This will be referenced by every downstream document that produces client-facing copy."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "This document is a reference toolkit — "
                "every section should be independently useful. "
                "Headlines and vocabulary lists as <ul>. "
                "Comparison matrices as HTML <table> elements. "
                "All content scannable — no long prose paragraphs."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/u5_positioning_map.html",
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate JSON for a 2×2 positioning map.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "axis_x": {"label": "Axis label", "low": "Low end", "high": "High end"},\n'
                '  "axis_y": {"label": "Axis label", "low": "Low end", "high": "High end"},\n'
                '  "positions": [\n'
                '    {"name": "Your Business", "x": 0.8, "y": 0.7, "highlight": true},\n'
                '    {"name": "Competitor A", "x": 0.3, "y": 0.5, "highlight": false},\n'
                '    {"name": "DIY", "x": 0.1, "y": 0.2, "highlight": false},\n'
                '    {"name": "Do Nothing", "x": 0.0, "y": 0.0, "highlight": false}\n'
                "  ]\n"
                "}\n"
                "```\n"
                "Choose axes that best differentiate this client from alternatives."
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q3", "Q5", "Q7", "Q8", "Q9",
        "Q10", "Q32", "Q33", "Q34", "Q35", "Q36", "Q37",
        "Q49",
    ],
    upstream_deps=[DocID.U1, DocID.U2, DocID.U3],
    downstream_consumers=[
        DocID.U6,
        DocID.BM1, DocID.BM5,
        DocID.FC1, DocID.FC3,
        DocID.CH1, DocID.CH2, DocID.CH3, DocID.CH4,
    ],
    maturity_adaptations={
        Maturity.STARTER: (
            "Help them discover their positioning. They likely haven't articulated it before. "
            "Frame as 'hypothesis to test in market' not 'final positioning.' "
            "Simpler vocabulary — don't overwhelm with 10 angles."
        ),
        Maturity.GROWING: (
            "Sharpen informal positioning into explicit messaging. "
            "They know what works from experience — extract and formalize it. "
            "Kill the 'we do everything for everyone' tendency."
        ),
        Maturity.ESTABLISHED: (
            "Refine and defend position. May need to NARROW — success often leads to scope creep. "
            "Premium positioning should be explicit. 'We're expensive, and here's why' is valid messaging."
        ),
        Maturity.PIVOT: (
            "Bridge positioning: 'X years in [old domain] taught me [transferable insight] "
            "that I now apply to [new domain].' Authority transfer is the key messaging move."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Positioning must be MEMORABLE and shareable. Emphasize one-line differentiation.",
        Bottleneck.LEAD_GENERATION: "Messaging angles are the priority — leads exist but don't engage.",
        Bottleneck.CONVERSION: "Focus on objection-handling messaging. What words build trust at decision point?",
        Bottleneck.PRICING: "Positioning must justify premium pricing. Value-based language over feature lists.",
        Bottleneck.RETENTION: "Standard depth — positioning is less critical for retention.",
        Bottleneck.WRONG_CLIENTS: (
            "THIS IS THE PRIORITY DOC. Positioning must REPEL wrong clients AND attract right ones. "
            "The vocabulary cheat sheet should include 'filter words' — terms that self-select the right audience."
        ),
    },
    quality_rules=[
        "Positioning statement must pass the 3 tests (specificity, so-what, proof). Don't ship one that fails.",
        "Headlines must sound natural and professional — no forced marketing jargon.",
        "The competitive matrix must be honest. Acknowledging a weakness and reframing it is stronger than pretending.",
        "Messaging angles must be DISTINCT. If angles 1 and 2 are both pain-first with different wording, that's one angle.",
        "Vocabulary lists must be specific to this business. Generic power words ('revolutionary', 'cutting-edge') are banned.",
        "The origin story must not sound manufactured. If insufficient personal info is available, provide the scaffold only.",
        "Tone guidelines must reflect how the actual OWNER communicates, not an idealized brand voice.",
    ],
)