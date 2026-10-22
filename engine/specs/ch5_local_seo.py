"""CH5: Local SEO & Maps Strategy.

When local IS the primary channel — deeper than BM3 baseline.
Full GBP strategy, review system, local content, citations, and backlinks.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH5_SPEC = DocSpec(
    id=DocID.CH5,
    name="Local SEO & Maps Strategy",
    tier=Tier.CHANNEL,
    purpose=(
        "Full local SEO strategy when local search is the PRIMARY acquisition channel. "
        "Extends BM3 baseline with review generation systems, local content, "
        "backlink strategy, competitor analysis, and Maps ranking optimization."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Local Search Landscape & Competitor Analysis",
            purpose="Understand who dominates local search and where the gaps are",
            tone_note="Data-driven. Name specific competitors and their strengths/weaknesses.",
            static_content=(
                "## How Local Search Works\n\n"
                "### The 3 Local Ranking Factors (Google)\n"
                "1. **Relevance**: How well your profile matches the search\n"
                "2. **Distance**: How close you are to the searcher\n"
                "3. **Prominence**: How well-known/trusted you are (reviews, links, citations)\n\n"
                "You can't change distance. You can optimize relevance and prominence.\n\n"
                "### Competitive Analysis Framework\n"
                "For each of the top 3 competitors in your local pack:\n"
                "- Number of Google reviews + average rating\n"
                "- GBP completeness (photos, posts, Q&A)\n"
                "- Website quality + local pages\n"
                "- Citation count (directory listings)\n"
                "- Backlink profile (local links)"
            ),
            dynamic_prompt=(
                "Analyze the local search landscape for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Location: {Q5}\n\n"
                "Produce:\n"
                "1. **Top 5-10 search terms** their customers use to find this type of business locally\n"
                "2. **Competitive gap analysis** framework (what to evaluate for each competitor)\n"
                "3. **Quick wins** available right now (where competitors are weak)\n"
                "4. **Long-term ranking factors** to build over 3-6 months"
            ),
        ),
        SectionSpec(
            name="Review Generation System",
            purpose="Systematically generate a stream of positive reviews",
            tone_note="Reviews are the #1 local ranking factor after relevance. This section is critical.",
            static_content=(
                "## The Review System\n\n"
                "### Why Reviews Matter (The Numbers)\n"
                "- 87% of consumers read online reviews for local businesses\n"
                "- Businesses with 50+ reviews earn 4.6% more revenue (Harvard Business School)\n"
                "- Review VELOCITY matters: 5 reviews/month > 50 reviews that stopped 2 years ago\n\n"
                "### The Ask Framework\n"
                "1. **Who to ask**: only satisfied customers (post-delivery, post-positive feedback)\n"
                "2. **When to ask**: at peak satisfaction (not 2 months later)\n"
                "3. **How to ask**: direct, specific, easy\n"
                "4. **Where to ask**: Google first, then industry-specific platforms\n\n"
                "### The Ask Script\n"
                "❌ 'Could you leave us a review?' (vague, ignorable)\n"
                "✅ 'Thanks so much for your trust! If you're happy with our work, "
                "a Google review helps us a lot. Here's the direct link: [URL]' "
                "(specific, easy, grateful)\n\n"
                "### What's Legal?\n"
                "- Asking for reviews: ✅ Legal everywhere\n"
                "- Incentivizing reviews: ⚠ Google prohibits (and can detect)\n"
                "- Buying/faking reviews: ❌ Illegal in most jurisdictions "
                "(FTC Act in US, consumer protection laws in EU/UK/AU)\n"
                "- Responding to negative reviews: ✅ Required (professionally)"
            ),
            dynamic_prompt=(
                "Build the review generation system for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Current proof: {Q32}\n"
                "- Customers/month: {Q19}\n\n"
                "Produce:\n"
                "1. **Peak satisfaction moments** for their business (when to ask)\n"
                "2. **Ask scripts**: verbal (in-person), SMS, email (full copy for each)\n"
                "3. **Google review link** generation instructions\n"
                "4. **Monthly target**: how many reviews to aim for, based on {Q19} customer volume\n"
                "5. **Negative review response templates** (3 scenarios: valid complaint, "
                "unfair review, competitor attack)\n"
                "6. **Platform priority order** for their industry\n\n"
                "Make the ask scripts sound natural. A plumber doesn't talk like a hotel concierge."
            ),
        ),
        SectionSpec(
            name="Local Content & Backlink Strategy",
            purpose="Build local authority through content and links",
            tone_note="Long-term play. Results in 3-6 months. But compounding value.",
            static_content=(
                "## Local Content Strategy\n\n"
                "### Content That Ranks Locally\n"
                "- **Service + Location pages**: '/plumber-downtown' not just '/services'\n"
                "- **Local guides**: 'Best [X] in [neighborhood]' — attracts local links\n"
                "- **FAQ pages**: answer questions people ask Google about your service\n"
                "- **Blog posts**: local events, community involvement, partnerships\n\n"
                "### Local Backlinks\n"
                "| Source | Difficulty | Impact |\n"
                "|--------|-----------|--------|\n"
                "| Local directories | Easy | Medium |\n"
                "| Chamber of commerce | Easy | Medium-High |\n"
                "| Local press / blogs | Medium | High |\n"
                "| Local partnerships | Medium | High |\n"
                "| Sponsorships (sports, events) | Easy-Medium | Medium |\n"
                "| University / school partnerships | Medium | High |"
            ),
            dynamic_prompt=(
                "Build the local content and backlink plan.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Location: {Q5}\n"
                "- Website: {Q28}\n\n"
                "Produce:\n"
                "1. **5 local landing page ideas** (service + location combinations)\n"
                "2. **3 local content ideas** (guides, FAQs, community pieces)\n"
                "3. **10 local backlink targets** specific to their location and industry\n"
                "4. **Schema markup recommendations** (LocalBusiness, Service, FAQ)\n"
                "5. **3-month local SEO action plan** (monthly priorities)"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment="Review scripts must be complete and ready to use.",
        ),
    ],
    relevant_questions=["Q1", "Q2", "Q5", "Q6", "Q19", "Q28", "Q29", "Q32"],
    upstream_deps=[DocID.U2, DocID.U5, DocID.BM3],
    downstream_consumers=[DocID.U6, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Focus on GBP + reviews. Content and backlinks are Phase 2.",
        Maturity.GROWING: "Full strategy: reviews + local content + citation expansion.",
        Maturity.ESTABLISHED: "Advanced: competitor gap analysis, schema markup, local content hub.",
        Maturity.PIVOT: "New local presence for new business. GBP creation + review sprint.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "This IS the solution. Maximum depth on all sections.",
        Bottleneck.LEAD_GENERATION: "Focus on conversion-oriented GBP features (booking, call, messages).",
        Bottleneck.CONVERSION: "Reviews and trust signals are the conversion lever in local.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Review requests double as retention touchpoints.",
        Bottleneck.WRONG_CLIENTS: "GBP categories and local pages must target the right audience.",
    },
    quality_rules=[
        "Review ask scripts must sound natural for the business type.",
        "Local keywords must be in english.",
        "Backlink targets must be genuinely local — not generic directories.",
        "Schema markup recommendations must be specific (which type, which fields).",
        "Monthly review targets must be realistic for their customer volume.",
        "Never recommend buying or faking reviews — it violates platform ToS and consumer protection laws.",
    ],
)