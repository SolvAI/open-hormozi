"""CH1: SEA Strategy (Google Ads).

For high-intent search acquisition: keyword research, campaign structure,
ad copy, bidding, budget, and specialist brief.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH1_SPEC = DocSpec(
    id=DocID.CH1,
    name="SEA Strategy (Google Ads)",
    tier=Tier.CHANNEL,
    purpose=(
        "Design a complete Google Ads strategy: keyword architecture, campaign structure, "
        "ad copy, bidding approach, budget allocation, and KPIs. "
        "Actionable enough to hand to a specialist or execute directly."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Keyword Architecture",
            purpose="Map high-intent keyword groups organized by buyer intent",
            tone_note="Specific to the client's domain. Not generic keyword research theory.",
            static_content=(
                "## Keyword Intent Tiers\n\n"
                "| Intent Level | What It Means | Example | CPC Tolerance |\n"
                "|-------------|---------------|---------|---------------|\n"
                "| **High intent** | Ready to buy/hire NOW | 'freelance react developer [city]' | Highest |\n"
                "| **Pain-aware** | Knows the problem, exploring solutions | 'how to reduce technical debt' | Medium |\n"
                "| **Competitor** | Comparing specific alternatives | '[competitor] vs [alternative]' | Medium-High |\n"
                "| **Informational** | Researching, not ready to buy | 'what is technical debt' | Low / avoid |\n\n"
                "### Match Types\n"
                "- **Exact match** [keyword]: highest relevance, lowest volume\n"
                "- **Phrase match** \"keyword\": moderate relevance + volume\n"
                "- **Broad match** keyword: Google's AI matching — only with smart bidding\n\n"
                "### Negative Keywords\n"
                "Critical for B2B: exclude 'free', 'internship', 'training', 'jobs', 'salary', 'tutorial', 'DIY'.\n"
                "Build your negative list BEFORE launching."
            ),
            dynamic_prompt=(
                "Build the keyword architecture for this client.\n\n"
                "Based on:\n"
                "- Service/product: {Q7}\n"
                "- Industry: {Q2}\n"
                "- Target customer: {Q34}\n"
                "- Problem solved: {Q35}\n"
                "- Alternatives: {Q37}\n"
                "- Geography: {Q5}\n"
                "- B2B target: {Q38}, {Q39}\n\n"
                "Produce:\n"
                "1. **4-6 keyword groups** organized by intent tier\n"
                "2. **10-15 keywords per group** (in english)\n"
                "3. **Match type recommendation** per group\n"
                "4. **20+ negative keywords** specific to their domain\n"
                "5. **Competitor keywords** (if competitors are searchable)\n\n"
                "Keywords must be in English."
            ),
        ),
        SectionSpec(
            name="Campaign & Ad Group Structure",
            purpose="Organize campaigns for clean data and easy optimization",
            tone_note="This determines how they'll read performance data. Structure matters more than copy.",
            static_content=(
                "## Campaign Structure Principles\n\n"
                "```\n"
                "Account\n"
                "├── Campaign: [Intent Level / Service Line]\n"
                "│   ├── Ad Group: [Keyword Theme]\n"
                "│   │   ├── Keywords (5-15 per group)\n"
                "│   │   ├── Ads (3-5 responsive search ads)\n"
                "│   │   └── Extensions\n"
                "│   └── Ad Group: [Another Theme]\n"
                "└── Campaign: [Another Intent / Service]\n"
                "```\n\n"
                "### Rules\n"
                "1. **One intent level per campaign** (don't mix high-intent and informational)\n"
                "2. **Tight ad groups**: 5-15 keywords that share a theme\n"
                "3. **Budget at campaign level**: allocate most to high-intent\n"
                "4. **Separate brand vs non-brand**: always\n"
                "5. **Start with 2-3 campaigns max**: add complexity after data"
            ),
            dynamic_prompt=(
                "Design the campaign structure for this client.\n\n"
                "Using the keyword groups above, create:\n"
                "1. **Campaign map**: name, intent level, budget %, keywords per group\n"
                "2. **Ad group breakdown** within each campaign\n"
                "3. **Budget allocation** (% of {Q44} total budget per campaign)\n"
                "4. **Priority order**: which campaign to launch first\n\n"
                "Start simple. If budget ({Q44}) < $2000/mo: max 2 campaigns. "
                "If > $3000: can justify 3-4."
            ),
        ),
        SectionSpec(
            name="Ad Copy",
            purpose="Write the actual ads — headlines, descriptions, extensions",
            tone_note="Google Ads has strict character limits. Every word must earn its place.",
            static_content=(
                "## Responsive Search Ad Format\n\n"
                "- **Headlines**: up to 15, max 30 chars each (Google tests combinations)\n"
                "- **Descriptions**: up to 4, max 90 chars each\n"
                "- **Display URL paths**: 2 paths, 15 chars each\n\n"
                "### Headline Formula\n"
                "Pin position 1: [Keyword / Service] — relevance\n"
                "Pin position 2: [Benefit / Differentiator] — persuasion\n"
                "Others: mix of social proof, CTA, urgency, features\n\n"
                "### Extensions to Always Use\n"
                "- **Sitelinks**: 4-6 (services, about, case studies, contact)\n"
                "- **Callouts**: 4-6 (free consultation, 10 years experience, etc.)\n"
                "- **Structured snippets**: service types, brands, etc.\n"
                "- **Call extension**: if phone calls matter\n"
                "- **Location extension**: if local"
            ),
            dynamic_prompt=(
                "Write Google Ads copy for this client.\n\n"
                "For each ad group defined above, produce:\n"
                "1. **8-10 headlines** (max 30 chars each) — mix of:\n"
                "   - Keyword-matching headlines\n"
                "   - Benefit headlines\n"
                "   - Proof headlines (from {Q33})\n"
                "   - CTA headlines\n"
                "2. **4 descriptions** (max 90 chars each)\n"
                "3. **Display URL paths** (e.g., /service/audit)\n"
                "4. **4 sitelink texts + descriptions**\n"
                "5. **6 callout texts** (25 chars each)\n\n"
                "All copy in English. "
                "Character counts MUST be respected — count them."
            ),
        ),
        SectionSpec(
            name="Bidding, Budget & KPIs",
            purpose="Set the financial parameters and success criteria",
            tone_note="Math-driven. Connect ad spend to expected clients and revenue.",
            static_content=(
                "## Bidding Strategies\n\n"
                "| Strategy | When to Use | Minimum Data |\n"
                "|----------|------------|-------------|\n"
                "| **Manual CPC** | Starting out, learning | None |\n"
                "| **Maximize clicks** | Need traffic data fast | None |\n"
                "| **Target CPA** | Know your cost-per-lead target | 30+ conversions/month |\n"
                "| **Maximize conversions** | Budget-constrained, want volume | 15+ conversions |\n"
                "| **Target ROAS** | E-commerce with revenue tracking | 50+ conversions |\n\n"
                "### Starting Recommendation\n"
                "Week 1-2: Manual CPC or Maximize Clicks (gather data).\n"
                "Week 3+: Switch to Target CPA once you have 15+ conversions.\n\n"
                "### Budget Rules\n"
                "- Minimum viable: $50/day ($1,500/mo) for B2B services\n"
                "- Don't spread too thin: better $50/day on 1 campaign than $15/day on 3\n"
                "- Daily budget = monthly / 30.4"
            ),
            dynamic_prompt=(
                "Set the bidding and budget strategy for this client.\n\n"
                "Based on:\n"
                "- Budget: {Q44}\n"
                "- Deal size: {Q10}\n"
                "- Margin: {Q22}\n"
                "- Target revenue: {Q40}\n\n"
                "Calculate:\n"
                "1. **Daily budget** and allocation per campaign\n"
                "2. **Target CPA** (max cost per lead that's profitable)\n"
                "3. **Expected CPC** range for their keywords (estimate by industry)\n"
                "4. **Expected funnel**: clicks → leads → clients → revenue per month\n"
                "5. **ROAS target** given their margin\n"
                "6. **Week 1-4 bidding plan**: which strategy, when to switch\n\n"
                "Show the complete waterfall:\n"
                "$X budget → ~Y clicks → ~Z leads → ~W clients → $V revenue → ROAS of N:1"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "All ad copy must respect "
                "character limits (count and verify). Include the full waterfall calculation."
            ),
        ),
        FormatSpec(
            format=Format.XLS,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            template_path="templates/excel/ch1_keyword_master.xlsx",
            prompt_fragment=(
                "Generate JSON to fill the keyword master template.\n"
                "Return ONLY valid JSON with this exact structure:\n"
                "```json\n"
                "{\n"
                '  "row_injections": [\n'
                '    {\n'
                '      "sheet": "Keyword Master List",\n'
                '      "start_row": 2,\n'
                '      "rows": [\n'
                '        ["keyword phrase", "Exact|Phrase|Broad", "ad group name", "campaign name", "High|Pain-aware|Competitor|Info", estimated_cpc_number, estimated_monthly_volume_number, "High|Medium|Low", "High|Medium|Low", "To launch", ""],\n'
                '        ...\n'
                '      ]\n'
                '    },\n'
                '    {\n'
                '      "sheet": "Negative Keywords",\n'
                '      "start_row": 2,\n'
                '      "rows": [\n'
                '        ["negative keyword", "Exact|Phrase|Broad", "Campaign name or All", "reason for exclusion"],\n'
                '        ...\n'
                '      ]\n'
                '    },\n'
                '    {\n'
                '      "sheet": "Ad Groups Structure",\n'
                '      "start_row": 2,\n'
                '      "rows": [\n'
                '        ["campaign name", "ad group name", "theme / intent description", keyword_count_number, "Headline 1 (max 30 chars)", "Headline 2 (max 30 chars)", "Description (max 90 chars)"],\n'
                '        ...\n'
                '      ]\n'
                '    }\n'
                '  ]\n'
                "}\n"
                "```\n\n"
                "Rules:\n"
                "- Keyword Master List: 15-30 rows. Pre-fill ALL keywords from the strategy above.\n"
                "  Column order: Keyword, Match Type, Ad Group, Campaign, Intent Level, Est. CPC, Est. Monthly Volume, Competition, Priority, Status, Notes.\n"
                "  CPC and Volume as raw numbers. Status = 'To launch' for all.\n"
                "- Negative Keywords: 15-25 rows. All domain-specific negatives from the strategy.\n"
                "  Column order: Negative Keyword, Match Type, Campaign / Ad Group, Reason.\n"
                "- Ad Groups Structure: 1 row per ad group defined in the strategy.\n"
                "  Column order: Campaign, Ad Group, Theme / Intent, Keywords (count), Headline 1, Headline 2, Description.\n"
                "  Headlines ≤30 chars, Description ≤90 chars. Count them.\n"
                "- All text in English. No currency symbols in numeric cells."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/ch1_ad_preview.html",
            model_tier=ModelTier.LIGHT,
            prompt_fragment=(
                "Generate JSON for Google Ads preview mockups.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "ads": [\n'
                '    {"headline1": "...", "headline2": "...", "headline3": "...",\n'
                '     "description1": "...", "description2": "...",\n'
                '     "display_url": "example.com/path1/path2",\n'
                '     "sitelinks": ["Link 1", "Link 2", "Link 3", "Link 4"]}\n'
                "  ]\n"
                "}\n"
                "```\n"
                "Include 2-3 ad previews representing different ad groups."
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q5", "Q7", "Q10",
        "Q22", "Q33", "Q34", "Q35", "Q37",
        "Q38", "Q39", "Q40", "Q44",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U7, DocID.U8, DocID.FC1, DocID.FC5],
    maturity_adaptations={
        Maturity.STARTER: "Conservative budget. 1-2 campaigns max. Manual CPC to learn. Heavy negative keywords.",
        Maturity.GROWING: "Full campaign structure. Move to smart bidding as data accumulates.",
        Maturity.ESTABLISHED: "Advanced: competitor campaigns, remarketing lists, Performance Max consideration.",
        Maturity.PIVOT: "New keywords for new domain. Leverage old brand if transferable.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "This IS the fix. Maximum budget allocation to high-intent keywords.",
        Bottleneck.LEAD_GENERATION: "Focus on pain-aware keywords + strong LP (FC1).",
        Bottleneck.CONVERSION: "Traffic exists — focus on ad-to-LP message match and remarketing.",
        Bottleneck.PRICING: "Standard depth. Ads drive to the redesigned pricing page.",
        Bottleneck.RETENTION: "Not the priority channel for retention. Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Negative keywords are critical. Filter at the keyword level.",
    },
    quality_rules=[
        "All headlines must be ≤30 characters. Count them. No exceptions.",
        "All descriptions must be ≤90 characters.",
        "Keywords must be in English.",
        "Negative keyword list must include industry-specific terms, not just generic ones.",
        "Budget waterfall must show specific numbers: clicks → leads → clients → revenue.",
        "CPC estimates must be industry-realistic, not generic '$1-3' for everything.",
        "If budget < $1,500/mo: explicitly state this is below recommended minimum and adjust expectations.",
    ],
)