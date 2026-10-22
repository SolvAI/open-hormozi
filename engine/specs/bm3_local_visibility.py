"""BM3: Local Visibility Baseline.

Table-stakes digital presence for any business with a physical location.
This is the foundation — regardless of chosen channel.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


BM3_SPEC = DocSpec(
    id=DocID.BM3,
    name="Local Visibility Baseline",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Establish the minimum viable local digital presence: Google Business Profile, "
        "directories, NAP consistency, photos, and categories. "
        "This is table stakes for any physical-location business regardless of channel strategy."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Google Business Profile Optimization",
            purpose="The single most important local asset — optimize every field",
            tone_note="Step-by-step. Many local businesses have a GBP but it's half-filled.",
            static_content=(
                "## Google Business Profile Is Your #1 Local Asset\n\n"
                "For local businesses, GBP drives more leads than your website. "
                "When someone searches '[service] near me', Google shows the Map Pack first — "
                "your GBP profile IS your first impression.\n\n"
                "### The Complete GBP Checklist\n"
                "| Element | Status | Impact |\n"
                "|---------|--------|--------|\n"
                "| Business name (exact legal name) | Must match everywhere | High |\n"
                "| Primary category | Most specific option available | Critical |\n"
                "| Secondary categories (up to 9) | All relevant ones selected | High |\n"
                "| Description (750 chars) | Keyword-rich, benefit-focused | Medium |\n"
                "| Hours (regular + special) | Always accurate | High |\n"
                "| Phone number | Matches website + directories | High |\n"
                "| Website URL | Points to relevant page | High |\n"
                "| Photos (20+ quality photos) | Updated quarterly | High |\n"
                "| Services/menu | Listed with prices | Medium |\n"
                "| Attributes | All relevant ones checked | Medium |\n"
                "| Q&A | Pre-seed with 5-10 common questions | Medium |\n"
                "| Posts | Weekly updates (offers, events, photos) | Medium |\n\n"
                "### The #1 Mistake: Wrong Category\n"
                "Your primary category determines 80% of which searches show your listing. "
                "'Restaurant' vs 'French restaurant' vs 'Bistro' → completely different results."
            ),
            dynamic_prompt=(
                "Build the GBP optimization plan for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Location context: {Q5}, {Q6}\n"
                "- Current website: {Q28}, {Q29}\n\n"
                "Produce:\n"
                "1. **Primary category recommendation** (the most specific available)\n"
                "2. **5 secondary categories** ranked by relevance\n"
                "3. **Business description** (full 750-char text, keyword-optimized)\n"
                "4. **Photo shot list**: 15-20 specific photos to take "
                "(e.g., 'storefront from street view', 'team at work', 'signature product close-up')\n"
                "5. **5 pre-seeded Q&A** with answers\n"
                "6. **Weekly post ideas** (4 templates they can rotate)\n\n"
                "Adapt recommendations to their specific business type and industry."
            ),
        ),
        SectionSpec(
            name="Directory & Citation Setup",
            purpose="Ensure consistent presence across all relevant directories",
            tone_note="Checklist-driven. This is grunt work, not strategy. Make it easy to execute.",
            static_content=(
                "## NAP Consistency = Trust Signal\n\n"
                "**NAP** = Name, Address, Phone. These must be IDENTICAL everywhere:\n"
                "- Google Business Profile\n"
                "- Your website\n"
                "- Every directory listing\n"
                "- Social media profiles\n\n"
                "Even small differences hurt: abbreviations, phone format variations, "
                "or inconsistent suite/unit numbers.\n\n"
                "### Priority Directories (Universal)\n"
                "| Directory | Priority | Cost | Time to List |\n"
                "|-----------|----------|------|-------------|\n"
                "| Google Business Profile | Critical | Free | 1-2 weeks verification |\n"
                "| Apple Maps (Apple Business Connect) | High | Free | 1 week |\n"
                "| Yelp | High | Free | 1-2 days |\n"
                "| Facebook Business | High | Free | Immediate |\n"
                "| Bing Places | Medium-High | Free | 1-2 weeks |\n"
                "| Waze | Medium | Free | 1-2 weeks |\n"
                "| Industry-specific directories | High | Varies | Varies |\n\n"
                "### The 80/20: Do These 5 First\n"
                "1. Google Business Profile\n"
                "2. Apple Business Connect\n"
                "3. Yelp\n"
                "4. Facebook Business Page\n"
                "5. #1 industry-specific directory for your vertical"
            ),
            dynamic_prompt=(
                "Build the directory checklist for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Location: {Q5}\n\n"
                "Produce:\n"
                "1. **Top 10 directories** ranked by priority for their specific industry "
                "and geographic market\n"
                "   (a restaurant has different directories than a plumber — "
                "include region-specific platforms relevant to their location)\n"
                "2. **Exact NAP format** to use everywhere (standardize once)\n"
                "3. **Industry-specific directories** (e.g., Healthgrades for doctors, "
                "TripAdvisor for restaurants, Houzz for home services, Avvo for lawyers — "
                "select platforms relevant to the client's industry and market)\n"
                "4. **Setup time estimate** for each directory\n\n"
                "Be specific to their industry and location — not a generic directory list."
            ),
        ),
        SectionSpec(
            name="Photo & Visual Asset Guide",
            purpose="Specific photo requirements for local profiles",
            tone_note="Actionable. They should be able to hand this to a photographer or do it themselves.",
            static_content=(
                "## Photos Drive Clicks\n\n"
                "GBP listings with 100+ photos get 520% more calls than those with fewer than 10 (BrightLocal).\n\n"
                "### Photo Types to Capture\n"
                "1. **Exterior**: storefront from street view (how to find you)\n"
                "2. **Interior**: atmosphere, décor, workspace\n"
                "3. **Team**: real people, not stock photos\n"
                "4. **Product/Service**: what the customer actually gets\n"
                "5. **Process**: behind the scenes, work in progress\n"
                "6. **Results**: before/after, finished projects, happy customers\n\n"
                "### Quality Rules\n"
                "- Natural light > flash\n"
                "- Landscape orientation for GBP\n"
                "- Minimum 720px wide\n"
                "- No heavy filters or text overlays\n"
                "- Update quarterly (seasonal relevance)"
            ),
            dynamic_prompt=(
                "Create a specific photo shot list for this client.\n\n"
                "Based on {Q1} and {Q2}, list 15-20 specific photos they should take.\n"
                "Not generic — specific:\n"
                "- Restaurant: 'signature dish close-up with natural light', "
                "'chef plating in the kitchen', 'outdoor seating area'\n"
                "- Tradesperson: 'before/after project photos', 'branded vehicle', "
                "'team on a job site with safety equipment'\n"
                "- Salon: 'styling station detail shot', 'client getting a haircut (with permission)', "
                "'product shelf display'\n\n"
                "For each photo: subject, framing tip, where it will be used (GBP, website, social)."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "GBP description must be "
                "a complete 750-char text ready to paste in a <blockquote>. "
                "Photo shot list as an <ol>. Directory list as an HTML <table>."
            ),
        ),
    ],
    relevant_questions=["Q1", "Q2", "Q5", "Q6", "Q28", "Q29"],
    upstream_deps=[DocID.U2, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: "Start from scratch. Step-by-step GBP creation guide.",
        Maturity.GROWING: "Likely have a basic GBP. Focus on optimization and expansion.",
        Maturity.ESTABLISHED: "Review and refresh. May have stale info or missing categories.",
        Maturity.PIVOT: "New GBP for new business, or update existing one for new positioning.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "THIS IS CRITICAL. GBP optimization is the single fastest win for local visibility.",
        Bottleneck.LEAD_GENERATION: "GBP posts and Q&A become lead generation tools.",
        Bottleneck.CONVERSION: "Standard depth. GBP reviews affect trust (see MT1).",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Standard depth. GBP posts can announce loyalty programs.",
        Bottleneck.WRONG_CLIENTS: "GBP description and categories must attract the right local audience.",
    },
    quality_rules=[
        "GBP description must be a complete, ready-to-paste 750-character text.",
        "NAP format must be standardized with exact punctuation and formatting.",
        "Directory list must be industry-specific — not the same list for every business.",
        "Photo shot list must be specific enough that someone can execute it in one afternoon.",
        "Don't recommend directories that are irrelevant to the business type.",
    ],
)