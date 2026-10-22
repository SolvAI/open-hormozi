"""U8: KPI & Tracking Framework.

What to measure at each funnel stage, how to track it,
and when to act on the numbers.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U8_SPEC = DocSpec(
    id=DocID.U8,
    name="KPI & Tracking Framework",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Define the metrics that matter at each funnel stage, set up tracking, "
        "and create decision rules that tell the client exactly what to look at, "
        "when, and what to do about it. Adapted to the funnel shape from U6."
    ),
    model_tier=ModelTier.HEAVY,
    sections=[
        SectionSpec(
            name="Metrics Hierarchy",
            purpose="Separate leading indicators from lagging indicators and vanity metrics",
            tone_note="STARTER: explain why followers ≠ revenue. ESTABLISHED: skip to their specific metrics.",
            static_content=(
                "## The Metrics That Actually Matter\n\n"
                "### Three Categories\n"
                "| Category | What It Tells You | Examples | Action If Bad |\n"
                "|----------|--------------------|----------|---------------|\n"
                "| **North Star** | Is the business healthy? | Monthly revenue, profit, active clients | Alarm — investigate everything |\n"
                "| **Leading indicators** | Will NEXT month be healthy? | Leads/week, calls booked, conversion rate | Fix now before it's too late |\n"
                "| **Vanity metrics** | Nothing useful | Followers, page views, impressions | Ignore unless tied to revenue |\n\n"
                "### The Dangerous Middle\n"
                "Most businesses track either too little (only revenue) or too much (50 metrics, no action). "
                "The right number is **5-8 metrics** that form a complete chain from awareness to revenue.\n\n"
                "### The Funnel Chain\n"
                "```\n"
                "Impressions → Clicks → Leads → Qualified → Closed → Revenue → Retained → Referred\n"
                "```\n"
                "Track the conversion RATE between each step. The weakest rate is your bottleneck."
            ),
            dynamic_prompt=(
                "Build the metrics hierarchy for this client.\n\n"
                "Based on:\n"
                "- Funnel shape from U6\n"
                "- Channel: {channel}\n"
                "- Business type: {Q1}\n"
                "- Bottleneck: {bottleneck}\n\n"
                "Define:\n"
                "1. **North Star metric** (the ONE number that best represents business health)\n"
                "2. **5-7 leading indicators** mapped to funnel stages\n"
                "3. **Vanity metrics to STOP tracking** (name them explicitly)\n\n"
                "For each leading indicator, specify:\n"
                "- What it measures\n"
                "- Where to find it (which tool/dashboard)\n"
                "- Target value (from U6 benchmarks and U7 model)\n"
                "- Red flag threshold (below this = take action)\n\n"
                "If {Q1} = restaurant: metrics are covers/day, avg ticket, "
                "review score, repeat visit rate — NOT website traffic.\n"
                "If {Q1} = e-commerce: metrics are sessions, add-to-cart rate, "
                "checkout completion, AOV, repeat rate."
            ),
        ),
        SectionSpec(
            name="Tracking Setup",
            purpose="Specify exactly what tool tracks what metric",
            tone_note="Practical. Match tools to their tech level. No overkill.",
            static_content=(
                "## Tracking Stack by Complexity\n\n"
                "| Level | Tools | Cost | Setup Time |\n"
                "|-------|-------|------|------------|\n"
                "| **Basic** | Google Analytics + Google Sheets | Free | 2-3 hours |\n"
                "| **Intermediate** | GA4 + CRM (HubSpot free) + UTM tracking | Free-$50/mo | 1 day |\n"
                "| **Advanced** | GA4 + CRM + Looker Studio + conversion tracking | $50-200/mo | 2-3 days |\n\n"
                "### Non-Negotiable Setup (regardless of level)\n"
                "1. **UTM parameters** on every link you share or advertise\n"
                "2. **Conversion tracking** on your most important action (purchase, form, call)\n"
                "3. **A single spreadsheet** where weekly numbers live (even if you have dashboards)\n\n"
                "### Why the Spreadsheet Matters\n"
                "Dashboards are great but dangerous — you glance at them without thinking. "
                "Manually entering 5 numbers into a spreadsheet every Monday morning forces you to NOTICE trends."
            ),
            dynamic_prompt=(
                "Recommend the tracking setup for this client.\n\n"
                "Based on:\n"
                "- Tech comfort: {Q47}\n"
                "- Budget: {Q44}\n"
                "- Current tools: {Q28} (website), {Q31} (social)\n"
                "- Team size: {Q4}\n\n"
                "Specify:\n"
                "1. **Recommended tracking level** (basic/intermediate/advanced)\n"
                "2. **Tool per metric**: which tool provides which number\n"
                "3. **Setup checklist**: step-by-step what to configure\n"
                "4. **UTM structure**: specific UTM naming convention for their campaigns\n\n"
                "If {Q47} includes 'none of the above': Level Basic only. "
                "The spreadsheet IS the dashboard. Don't prescribe GA4 event tracking "
                "to someone who can't build a landing page."
            ),
        ),
        SectionSpec(
            name="Reporting Cadence & Decision Rules",
            purpose="When to look at what, and what action to take",
            tone_note="This is the operational core. 'Every Monday, look at X. If below Y, do Z.'",
            static_content=(
                "## The Review Rhythm\n\n"
                "| When | What to Check | Time Needed |\n"
                "|------|--------------|-------------|\n"
                "| **Daily** (optional) | Ad spend, lead count | 5 min |\n"
                "| **Weekly** (required) | Full funnel numbers, conversion rates, spend vs budget | 15-30 min |\n"
                "| **Monthly** | Revenue vs target, CAC, LTV, trend analysis | 1-2 hours |\n"
                "| **Quarterly** | Strategy review: is the channel working? Pivot needed? | Half day |\n\n"
                "### The Decision Matrix\n"
                "For each metric, define THREE zones:\n"
                "- 🟢 **Green**: on track → keep going, no changes\n"
                "- 🟡 **Yellow**: below target but above red → investigate, small adjustments\n"
                "- 🔴 **Red**: below minimum → stop, diagnose, fix before continuing\n\n"
                "### The Monday Morning Routine\n"
                "1. Open your tracking spreadsheet\n"
                "2. Enter this week's numbers\n"
                "3. Check: any metric in 🔴?\n"
                "4. If yes: that's your ONLY priority this week\n"
                "5. If all 🟢: continue execution, consider scaling"
            ),
            dynamic_prompt=(
                "Build the complete reporting cadence for this client.\n\n"
                "For each metric defined in the hierarchy above:\n"
                "1. **Review frequency** (daily / weekly / monthly)\n"
                "2. **Green zone** (target range)\n"
                "3. **Yellow zone** (watch range)\n"
                "4. **Red zone** (action required)\n"
                "5. **Red zone response**: specific action to take if metric hits red\n\n"
                "Format as a decision table:\n"
                "| Metric | Frequency | 🟢 Green | 🟡 Yellow | 🔴 Red | Red Action |\n\n"
                "Calibrate to their time availability ({Q45}) — don't prescribe daily reviews "
                "for someone with 2 hours/week total. Batch into the weekly review.\n\n"
                "End with: 'The single most important 15 minutes of your week is the Monday review.'"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate the complete KPI framework. "
                "The decision matrix as an HTML <table> with specific numbers for this client. "
                "Include the Monday Morning Routine as an <ol> checklist."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q10", "Q18", "Q19",
        "Q28", "Q31", "Q40",
        "Q44", "Q45", "Q47",
    ],
    upstream_deps=[DocID.U1, DocID.U6, DocID.U7],
    downstream_consumers=[DocID.U9],
    maturity_adaptations={
        Maturity.STARTER: (
            "Keep it to 5 metrics max. Spreadsheet tracking only. "
            "The goal is building the HABIT of tracking, not building a dashboard."
        ),
        Maturity.GROWING: (
            "Full framework. Introduce CRM tracking if not already present. "
            "Weekly + monthly cadence."
        ),
        Maturity.ESTABLISHED: (
            "Advanced tracking. May already have tools — optimize what they have. "
            "Add LTV cohort analysis and churn tracking."
        ),
        Maturity.PIVOT: (
            "Start fresh. New metrics for new business. Don't carry over old KPIs "
            "that don't apply."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Emphasize top-of-funnel metrics: impressions, reach, click-through rate.",
        Bottleneck.LEAD_GENERATION: "Emphasize mid-funnel: lead volume, lead quality score, cost per lead.",
        Bottleneck.CONVERSION: "Emphasize bottom-funnel: close rate, proposal-to-close, objection frequency.",
        Bottleneck.PRICING: "Emphasize revenue-per-client: AOV, revenue per deal, discount frequency.",
        Bottleneck.RETENTION: "Emphasize retention metrics: repeat rate, churn, LTV, reactivation rate.",
        Bottleneck.WRONG_CLIENTS: "Emphasize quality metrics: client satisfaction, project scope creep, referral rate.",
    },
    quality_rules=[
        "Maximum 8 metrics. More than 8 means nothing gets attention.",
        "Every metric must have a specific target number, not 'improve' or 'increase'.",
        "Decision rules must be binary: 'If X < Y, do Z.' Not 'consider adjusting if appropriate.'",
        "Tracking setup must be achievable in a single afternoon for the basic level.",
        "If the client tracks nothing today, the first action is 'start a spreadsheet this week'.",
        "Vanity metrics must be named and killed explicitly — 'Stop checking your Instagram follower count.'",
    ],
)