"""FC2: Lead Magnet.

The free resource that captures email addresses and qualifies leads:
topic, full outline, design brief, delivery automation, follow-up.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


FC2_SPEC = DocSpec(
    id=DocID.FC2,
    name="Lead Magnet",
    tier=Tier.FUNNEL,
    purpose=(
        "Design and outline a lead magnet that attracts the right audience, "
        "demonstrates expertise, and creates natural demand for the paid offer. "
        "Includes topic selection, full content outline, design brief, "
        "delivery automation, and follow-up sequence."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Topic & Format Selection",
            purpose="Choose a lead magnet topic that attracts buyers, not freebie-seekers",
            tone_note="The lead magnet must FILTER, not just attract. Quality over quantity.",
            static_content=(
                "## The Lead Magnet Test\n\n"
                "A great lead magnet passes 3 tests:\n"
                "1. **Relevance test**: Does it attract your IDEAL buyer specifically?\n"
                "   - ❌ '10 Tips for Better Marketing' (attracts everyone, converts no one)\n"
                "   - ✅ 'The CTO's Checklist: 7 Signs Your Codebase Needs a Senior Dev' (attracts CTOs)\n"
                "2. **Value test**: Is it useful enough that they'd pay $20-50 for it?\n"
                "3. **Bridge test**: Does it naturally lead to wanting your paid offer?\n\n"
                "### Lead Magnet Formats (Ranked by Conversion)\n"
                "| Format | Effort | Conversion | Best For |\n"
                "|--------|--------|-----------|----------|\n"
                "| **Checklist / Cheat Sheet** | Low | High | Quick wins, processes |\n"
                "| **Template / Swipe File** | Low-Medium | High | Tools, frameworks |\n"
                "| **Mini-Course (email)** | Medium | High | Education-dependent sales |\n"
                "| **Calculator / Tool** | High | Very High | Number-driven decisions |\n"
                "| **PDF Guide** | Medium | Medium | Authority building |\n"
                "| **Webinar / Video** | High | Medium | See FC3 for full treatment |\n"
                "| **Quiz / Assessment** | Medium-High | Very High | Personalized results |\n\n"
                "### The Hormozi Rule\n"
                "Give away the WHAT and the WHY. Sell the HOW.\n"
                "'Here's exactly what you need to do (checklist). Want us to do it for you? That's our service.'"
            ),
            dynamic_prompt=(
                "Select the lead magnet topic and format for this client.\n\n"
                "Based on:\n"
                "- ICP pains from U2: {Q35}, {Q36}\n"
                "- What they sell: {Q7}\n"
                "- Target audience: {Q34}\n"
                "- Current alternatives: {Q37}\n"
                "- Deal size: {Q10} (higher = more investment in lead magnet)\n"
                "- Sales cycle: {Q16}\n\n"
                "Produce:\n"
                "1. **Recommended topic** with rationale (pass the 3 tests above)\n"
                "2. **Format** with rationale\n"
                "3. **Title** (using headline formulas from U5)\n"
                "4. **2 alternative topics** they could test later\n"
                "5. **Bridge logic**: how this leads naturally to the paid offer\n\n"
                "The lead magnet must solve a NARROW problem completely, "
                "not give a broad overview of everything."
            ),
        ),
        SectionSpec(
            name="Content Outline",
            purpose="Full structure so the client can create it quickly",
            tone_note="Detailed enough to write in one sitting. Not just section headings.",
            static_content=(
                "## Content Outline Structure\n\n"
                "Every lead magnet follows:\n"
                "1. **Hook page** (title, subtitle, 'what you'll get')\n"
                "2. **Context** (why this matters — 1 paragraph)\n"
                "3. **Core content** (the actual value — 3-7 sections)\n"
                "4. **Next step** (bridge to paid offer)\n"
                "5. **About** (1 paragraph about the author + credibility)\n\n"
                "### Length Guidelines\n"
                "- Checklist: 1-3 pages\n"
                "- Template: 1-5 pages + instructions\n"
                "- Guide: 5-15 pages (NO MORE — nobody reads 50-page PDFs)\n"
                "- Mini-course: 3-5 emails over 5-7 days"
            ),
            dynamic_prompt=(
                "Build the complete content outline for the chosen lead magnet.\n\n"
                "Produce:\n"
                "1. **Title page copy** (title, subtitle, 3 bullet 'what you'll learn')\n"
                "2. **Section-by-section outline**:\n"
                "   - Section heading\n"
                "   - 3-5 key points to cover in each section\n"
                "   - Any frameworks/templates/checklists to include\n"
                "3. **Bridge to paid offer** (the last section — not salesy, but natural)\n"
                "4. **Author bio** (1 paragraph using {Q33} results)\n"
                "5. **Design brief**: style, colors, layout notes "
                "(clean and professional, not over-designed)\n\n"
                "The outline must be detailed enough that the client (or a writer) "
                "can produce the content in 2-4 hours."
            ),
        ),
        SectionSpec(
            name="Delivery & Follow-Up Automation",
            purpose="How the lead magnet gets delivered and what happens next",
            tone_note="Automation setup must match their tech level. Don't over-engineer.",
            static_content=(
                "## The Delivery System\n\n"
                "### Immediate Delivery Flow\n"
                "```\n"
                "Form Submit → Thank You Page → Email with Download Link\n"
                "```\n"
                "- **Thank you page**: confirms delivery + sets expectations for follow-up emails\n"
                "- **Email**: instant delivery (not 'we'll send it within 24h')\n"
                "- **Download link**: direct link to hosted file (Google Drive, Notion, own hosting)\n\n"
                "### Post-Download Nurture (3-5 emails)\n"
                "| Email | When | Content |\n"
                "|-------|------|--------|\n"
                "| 1 | Immediately | Delivery + 'start here' instructions |\n"
                "| 2 | Day 2 | Key insight from the lead magnet + 'did you try this?' |\n"
                "| 3 | Day 4 | Case study or additional value |\n"
                "| 4 | Day 7 | Bridge to offer: 'If you want help implementing this…' |\n"
                "| 5 | Day 10 | Soft CTA: book a call / check the offer |\n\n"
                "### Tools\n"
                "- Form: Tally, Typeform, ConvertKit, or native LP builder\n"
                "- Email: ConvertKit, Mailchimp, Brevo (ex-Sendinblue)\n"
                "- Hosting: Google Drive, Notion, or own site"
            ),
            dynamic_prompt=(
                "Design the delivery and follow-up system.\n\n"
                "Based on:\n"
                "- Tech comfort: {Q47}\n"
                "- Existing email list: {Q30}\n"
                "- Budget: {Q44}\n\n"
                "Produce:\n"
                "1. **Recommended tools** for form + email + hosting (matched to tech level)\n"
                "2. **Thank you page copy** (full text)\n"
                "3. **5-email follow-up sequence** (full copy for each):\n"
                "   - Subject lines\n"
                "   - Body text\n"
                "   - CTA per email\n"
                "4. **Setup checklist**: step-by-step to get this working\n"
                "5. **Timing and triggers** for each automation step\n\n"
                "If {Q47} = 'none of the above': use simplest possible stack "
                "(Tally form → manual email). Automate later."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "This is the STRATEGY document about the lead magnet — not the lead magnet itself.\n"
                "Use <h2> for major sections, <h3> for subsections, <table> for comparisons.\n"
                "All follow-up emails must be complete copy with subject lines in <blockquote> blocks.\n"
                "Tool recommendations as an HTML <table>.\n\n"
                "End with an <h2>Implementation Guide</h2> section in one paragraph that explains simply :\n"
                "Why do we need a lead magnet what is it for and how to put it in action concretely."
            ),
        ),
        FormatSpec(
            format=Format.PDF,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "You are generating the ACTUAL lead magnet PDF — the file the client's leads will download.\n"
                "This is NOT a strategy document. This is NOT an implementation guide.\n"
                "Do NOT include any meta-content about topic selection, delivery automation, tool setup, "
                "email sequences, or how to build/distribute the lead magnet.\n\n"
                "Output ONLY the lead magnet content itself:\n"
                "1. Title page (title, subtitle, 3 bullet 'what you'll learn')\n"
                "2. All content sections (the actual value — checklists, frameworks, templates, advice)\n"
                "3. About the author (1 short paragraph with proof from the client's results)\n"
                "4. Next step CTA (1 paragraph bridging to the paid offer — natural, not salesy)\n\n"
                "Write as if you ARE the client speaking to THEIR audience.\n"
                "The reader is the client's prospect — not the client themselves.\n"
                "All content must be specific to the client's domain. No generic filler.\n"
                "Professional layout with clean HTML typography. A4 format.\n"
                "Target 500-1500 words of genuinely useful content."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q10", "Q16",
        "Q30", "Q33", "Q34", "Q35", "Q36", "Q37",
        "Q44", "Q47",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: "Simple format (checklist/template). Create fast, test fast.",
        Maturity.GROWING: "More substantial (guide, mini-course). Leverage existing expertise.",
        Maturity.ESTABLISHED: "Premium lead magnets (calculator, assessment, video series).",
        Maturity.PIVOT: "Bridge content: draw on old domain expertise to attract new domain audience.",
    },
    bottleneck_adaptations={
        Bottleneck.LEAD_GENERATION: "THIS IS THE PRIORITY. The lead magnet IS the lead generation mechanism.",
        Bottleneck.VISIBILITY: "Lead magnet supports visibility through shareability and content marketing.",
        Bottleneck.CONVERSION: "Lead magnet warms leads before the sales conversation. Quality matters.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Lead magnet must FILTER. Topic specificity repels wrong audience.",
    },
    quality_rules=[
        "Lead magnet topic must pass all 3 tests (relevance, value, bridge).",
        "Content outline must be detailed enough to write in one sitting (2-4 hours).",
        "Follow-up emails must be complete copy — not 'send a reminder.'",
        "The PDF format is the ACTUAL lead magnet — it must be genuinely useful, not thin filler.",
        "Bridge to paid offer must feel natural, not a bait-and-switch.",
        "Title must be specific and outcome-driven, not generic.",
    ],
)