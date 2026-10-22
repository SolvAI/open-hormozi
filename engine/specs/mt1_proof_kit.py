"""MT1: Proof & Credibility Kit.

Systematize existing proof into deployable assets: case studies,
testimonial collection, logo walls, and proof stack assembly.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


MT1_SPEC = DocSpec(
    id=DocID.MT1,
    name="Proof & Credibility Kit",
    tier=Tier.MATURITY,
    purpose=(
        "Transform existing client results, testimonials, and credentials into "
        "a deployable proof arsenal. Case study templates, testimonial collection scripts, "
        "logo walls, and proof stack visuals ready to drop into LPs, proposals, and ads."
    ),
    model_tier=ModelTier.HEAVY,
    sections=[
        SectionSpec(
            name="Proof Inventory & Gap Analysis",
            purpose="Catalog all existing proof and identify what's missing",
            tone_note="Many clients HAVE proof but haven't documented it. Help them see what they already own.",
            static_content=(
                "## The Proof Hierarchy\n\n"
                "Not all proof is equal. Ranked by persuasive power:\n\n"
                "| Level | Type | Power | Example |\n"
                "|-------|------|-------|--------|\n"
                "| **1. Measurable results** | Highest | Numbers, before/after | 'Revenue +140% in 90 days' |\n"
                "| **2. Named testimonials** | Very High | Quote + name + photo + company | 'Thomas saved our launch — Marie, CTO Fintech.io' |\n"
                "| **3. Logos / brands** | High | Recognition, implied endorsement | Company logo wall |\n"
                "| **4. Volume metrics** | High | Scale indicator | '200+ clients served' |\n"
                "| **5. Credentials** | Medium | Certificates, awards, press | 'Featured in Les Echos' |\n"
                "| **6. Anonymous testimonials** | Low-Medium | Quote without attribution | 'Great experience!' — anonymous |\n"
                "| **7. Self-claims** | Lowest | You saying you're good | '10 years of experience' |\n\n"
                "### The Proof Stack\n"
                "Deploy proof at EVERY funnel stage:\n"
                "- **Ads**: short result + logo\n"
                "- **Landing page**: full case study + testimonial block + logo wall\n"
                "- **Sales call**: relevant case study for their industry\n"
                "- **Proposal**: 1-2 case studies matching their situation\n"
                "- **Follow-up emails**: drip case studies over time"
            ),
            dynamic_prompt=(
                "Build the proof inventory for this client.\n\n"
                "From:\n"
                "- Proof level: {Q32}\n"
                "- Concrete results: {Q33}\n"
                "- Website: {Q29}\n"
                "- Operating years: {Q3}\n\n"
                "Produce:\n"
                "1. **Existing proof inventory**: catalog everything they already have, "
                "ranked by the proof hierarchy\n"
                "2. **Gap analysis**: what's missing from each hierarchy level\n"
                "3. **Quick wins**: proof that EXISTS but isn't documented "
                "(e.g., a great result they mentioned in Q33 but never wrote up)\n"
                "4. **Priority list**: top 3 proof assets to create first\n\n"
                "Use {Q33} as raw material. Extract specific numbers, names, outcomes. "
                "If they wrote 'helped a client grow,' push for specifics in the case study."
            ),
        ),
        SectionSpec(
            name="Case Study Creation",
            purpose="Template and content for 2-3 case studies from existing results",
            tone_note="Case studies sell. A single detailed case study outperforms 100 feature bullets.",
            static_content=(
                "## The Case Study Framework: S.I.R.Q.\n\n"
                "### Structure\n"
                "1. **Situation**: Who was the client? What was their context?\n"
                "   - Industry, size, challenge they faced\n"
                "2. **Intervention**: What did you do? (process, not just deliverables)\n"
                "   - Timeline, approach, key decisions\n"
                "3. **Result**: What changed? (NUMBERS)\n"
                "   - Before → after, with specific metrics\n"
                "4. **Quote**: Client's own words about the experience\n"
                "   - If no formal quote: paraphrase what they said informally\n\n"
                "### Length Formats\n"
                "| Format | Length | Where to Use |\n"
                "|--------|--------|-------------|\n"
                "| **One-liner** | 1 sentence | Ads, social proof bars |\n"
                "| **Micro** | 3-4 sentences | LP testimonial section, email |\n"
                "| **Full** | 200-400 words | Dedicated page, proposal appendix |\n"
                "| **Deep dive** | 800+ words | Blog post, authority content |\n\n"
                "### Testimonial Collection Script\n"
                "Don't ask: 'Can you write me a testimonial?'\n"
                "Ask: 'Could you answer 3 quick questions about our work together?'\n"
                "1. What was your situation before working with me?\n"
                "2. What specific results did you get?\n"
                "3. What would you say to someone considering hiring me?"
            ),
            dynamic_prompt=(
                "Create 2-3 case studies from this client's existing results.\n\n"
                "Using {Q33} as raw material:\n\n"
                "For each case study:\n"
                "1. **One-liner version** (for ads and social proof bars)\n"
                "2. **Micro version** (3-4 sentences for LP testimonial blocks)\n"
                "3. **Full version** (200-400 words in S.I.R.Q. format)\n\n"
                "Where details are missing from {Q33}, mark with [ASK CLIENT: …] — "
                "specific questions they should ask the client to fill the gap.\n\n"
                "Also produce:\n"
                "4. **Testimonial request email** (full copy they can send to past clients)\n"
                "5. **3 follow-up questions** to deepen each case study\n\n"
                "Write case studies in the voice/language appropriate for their audience. "
                "A B2B case study sounds different from a restaurant review compilation."
            ),
        ),
        SectionSpec(
            name="Proof Asset Assembly",
            purpose="Package proof into ready-to-deploy visual assets",
            tone_note="These assets drop directly into LPs, proposals, pitch decks, and ads.",
            static_content=(
                "## Proof Assets to Create\n\n"
                "### 1. Logo Wall\n"
                "Grid of client/partner logos. Rules:\n"
                "- 6-12 logos (too few looks thin, too many looks cluttered)\n"
                "- All similar size, monochrome preferred (clean look)\n"
                "- Most recognizable logos first\n"
                "- Get permission (most clients are fine with it)\n\n"
                "### 2. Social Proof Bar\n"
                "One-line scrolling proof: '200+ clients | 4.8★ average | Featured in [press]'\n"
                "Goes right under the hero section of any page.\n\n"
                "### 3. Case Study Cards\n"
                "Visual cards (for LP and proposals):\n"
                "- Client name/logo | Challenge → Result | Quote\n"
                "- One card per case study\n\n"
                "### 4. Screenshot Gallery\n"
                "Screenshots of: Google reviews, LinkedIn recommendations, "
                "email thank-yous, social media mentions.\n"
                "Raw screenshots are MORE credible than designed testimonial blocks.\n\n"
                "### 5. Results Ticker\n"
                "Animated counter: '$X revenue generated | Y projects delivered | Z years experience'\n"
                "Only use numbers you can defend."
            ),
            dynamic_prompt=(
                "Design the proof asset package for this client.\n\n"
                "Based on:\n"
                "- Available proof from inventory above\n"
                "- Business type: {Q1}\n"
                "- Where proof will be used: LP (FC1), proposals (BM1), ads (CH1/CH2)\n\n"
                "Produce:\n"
                "1. **Logo wall content**: list of logos to include (from {Q33} client mentions)\n"
                "2. **Social proof bar text**: the one-liner for their LP\n"
                "3. **Case study card layout**: per case study from above\n"
                "4. **Screenshot collection list**: what screenshots to gather, from where\n"
                "5. **Results ticker numbers**: 3-4 defensible statistics about their work\n"
                "6. **Proof deployment map**: which asset goes WHERE in their funnel "
                "(ads → LP → call → proposal)\n\n"
                "If {Q32} = 'moderate': prioritize systematizing what exists over creating new proof."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Case studies must be complete "
                "in all three formats (one-liner, micro, full). "
                "Testimonial request email must be send-ready."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/mt1_case_study_card.html",
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate JSON for case study card visuals.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "cards": [\n'
                '    {"client_name": "...", "industry": "...", '
                '     "challenge": "One line", "result": "One line with numbers", '
                '     "quote": "Client quote...", "quote_author": "Name, Title"}\n'
                "  ]\n"
                "}\n"
                "```\n"
                "Include 2-3 cards. Use [LOGO PLACEHOLDER] for client logos."
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q3", "Q7",
        "Q29", "Q32", "Q33",
    ],
    upstream_deps=[DocID.U2, DocID.U5],
    downstream_consumers=[DocID.FC1, DocID.BM1, DocID.CH1, DocID.CH2],
    maturity_adaptations={
        Maturity.STARTER: "They may have very little proof. Focus on the testimonial request script and screenshot collection.",
        Maturity.GROWING: "Has results but hasn't documented them. This doc systematizes what exists.",
        Maturity.ESTABLISHED: "Rich proof library. Focus on organization, formatting, and strategic deployment.",
        Maturity.PIVOT: "Bridge proof: old domain results reframed for new domain credibility.",
    },
    bottleneck_adaptations={
        Bottleneck.CONVERSION: "Proof is the #1 conversion lever. Maximum depth. Deploy proof at every decision point.",
        Bottleneck.VISIBILITY: "Proof in ads increases CTR. Prioritize one-liners and social proof bars.",
        Bottleneck.LEAD_GENERATION: "Proof on LP increases form completion. Case study cards on LP.",
        Bottleneck.PRICING: "Strong proof justifies premium pricing. Connect to U4.",
        Bottleneck.RETENTION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Case studies should feature IDEAL clients — attracting more of the same.",
    },
    quality_rules=[
        "Case studies must have specific NUMBERS, not vague 'improved significantly.'",
        "Where numbers are missing, mark [ASK CLIENT] — don't fabricate.",
        "Testimonial request email must be send-ready — subject line, body, specific questions.",
        "Logo usage must mention getting permission from clients.",
        "Case study cards must be visually ready to drop into a landing page.",
        "Proof deployment map must show WHERE each asset goes in the funnel.",
    ],
)