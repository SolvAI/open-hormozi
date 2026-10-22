"""U7: Financial Model.

Investment breakdown, break-even analysis, projections, and
decision triggers for scaling or pivoting.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U7_SPEC = DocSpec(
    id=DocID.U7,
    name="Financial Model",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Build a complete financial model: investment required, fixed and variable costs, "
        "break-even calculation, conservative and optimistic projections, CAC vs LTV, "
        "and clear scaling triggers and kill-switch criteria."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Investment Breakdown",
            purpose="Total cost of implementing the strategy, itemized",
            tone_note="Honest. Include ALL costs, not just ad spend. Time cost is real cost.",
            static_content=(
                "## Total Investment = Money + Time\n\n"
                "Most financial plans only count ad spend. The real cost includes:\n\n"
                "### Money Costs\n"
                "- **Tools & subscriptions**: CRM, email, scheduling, hosting\n"
                "- **Paid acquisition**: ads, sponsored content\n"
                "- **Creative production**: design, copywriting, photography\n"
                "- **External help**: freelancers, agencies, consultants\n\n"
                "### Time Costs (convert to money)\n"
                "- **Your time**: hours/week × your effective hourly rate\n"
                "- **Team time**: if others are involved\n"
                "- **Learning curve**: first 2-4 weeks are slower\n\n"
                "### One-Time Setup vs Recurring\n"
                "Separate one-time investments (website, brand, initial creative) "
                "from monthly recurring costs (tools, ads, time). "
                "Your break-even calculation uses the recurring number."
            ),
            dynamic_prompt=(
                "Build the investment breakdown for this client's strategy.\n\n"
                "Based on:\n"
                "- Budget available: {Q44}\n"
                "- Time available: {Q45}\n"
                "- Channel: {channel} (each channel has different cost structure)\n"
                "- Triggered docs: {triggered_doc_list} (each implies tools/effort)\n"
                "- Tech comfort: {Q47}\n"
                "- Team size: {Q4}\n\n"
                "Produce an itemized table:\n"
                "| Item | One-Time | Monthly | Who |\n"
                "Show specific tool names and price ranges.\n"
                "Include the client's time valued at a reasonable rate "
                "(derive from {Q10} and {Q9} — if they charge $800/day, their time is worth $100/hr).\n\n"
                "Total it up: 'Month 1 total = $X (including $Y one-time setup). "
                "Months 2+ = $Z/mo recurring.'"
            ),
        ),
        SectionSpec(
            name="Break-Even Analysis",
            purpose="How many sales needed before the strategy pays for itself",
            tone_note="Math-forward. Show the exact calculation, not approximations.",
            static_content=(
                "## Break-Even Formula\n\n"
                "```\n"
                "Break-Even (units) = Monthly Fixed Costs / (Price per Unit - Variable Cost per Unit)\n"
                "Break-Even (time)  = Total Setup Costs / Monthly Net Profit from New Clients\n"
                "```\n\n"
                "### What Counts as Fixed vs Variable\n"
                "- **Fixed**: tool subscriptions, ad budget floor, your allocated time\n"
                "- **Variable**: per-client delivery costs, payment processing fees, bonuses/commissions\n\n"
                "### The Conservative Rule\n"
                "Always model with CONSERVATIVE conversion rates. "
                "If you break even on conservative numbers, you'll profit on realistic ones. "
                "If you only break even on optimistic numbers, you'll probably lose money."
            ),
            dynamic_prompt=(
                "Calculate break-even for this client.\n\n"
                "Inputs:\n"
                "- Recommended price from U4: use the designed tier prices\n"
                "- Monthly costs from Investment Breakdown above\n"
                "- Current margin: {Q22}\n"
                "- Channel conversion estimates from U6\n\n"
                "Show:\n"
                "1. **Break-even in deals**: how many new clients per month to cover strategy costs\n"
                "2. **Break-even in time**: months until cumulative revenue from new clients > total investment\n"
                "3. **Payback period**: when the strategy becomes net-positive\n\n"
                "Use THREE scenarios:\n"
                "- Conservative (50% of expected conversion rates)\n"
                "- Realistic (expected rates)\n"
                "- Optimistic (150% of expected rates)\n\n"
                "Present as a table with specific numbers, not ranges."
            ),
        ),
        SectionSpec(
            name="Revenue Projections",
            purpose="Month-by-month forecast for 6 months",
            tone_note="SURVIVAL: focus on 'when does cash arrive'. Others: steady growth model.",
            static_content=(
                "## Projection Methodology\n\n"
                "Month 1-2: ramp-up. Don't expect full performance.\n"
                "Month 3-4: reaching steady state. Optimization kicks in.\n"
                "Month 5-6: compounding — referrals, organic, reputation.\n\n"
                "### Assumptions to State Explicitly\n"
                "- Conversion rates (from U6 benchmarks)\n"
                "- Ramp-up factor (Month 1 = 50% of steady state)\n"
                "- Churn / repeat purchase rate\n"
                "- Price point used\n"
                "- Ad spend / lead volume\n\n"
                "**Any projection is only as good as its assumptions. State them clearly.**"
            ),
            dynamic_prompt=(
                "Build a 6-month revenue projection for this client.\n\n"
                "Starting point: {Q18} current revenue.\n"
                "Target: {Q40} by {Q41}.\n"
                "Channel: {channel} with expected ramp-up.\n"
                "Pricing: from U4 recommendations.\n"
                "Conversion: from U6 benchmarks.\n\n"
                "Month-by-month table:\n"
                "| Month | Ad Spend | Leads | Clients | New Revenue | Total Revenue | Cumulative Cost | Net |\n\n"
                "Show BOTH conservative and optimistic in side-by-side tables.\n"
                "Include existing revenue (not just new) for total picture.\n\n"
                "If {Q11} = repeat purchase: model retained revenue compounding month over month.\n"
                "If {Q15} = retainer: model recurring revenue accumulation."
            ),
        ),
        SectionSpec(
            name="Unit Economics: CAC, LTV, ROAS",
            purpose="The metrics that determine if the acquisition engine is profitable",
            tone_note="These are the HEALTH metrics. The client should check them monthly.",
            static_content=(
                "## The Three Numbers That Matter\n\n"
                "### CAC — Customer Acquisition Cost\n"
                "```\n"
                "CAC = Total Acquisition Spend / New Customers Acquired\n"
                "```\n"
                "Include ALL costs: ads + tools + time + creative.\n\n"
                "### LTV — Lifetime Value\n"
                "```\n"
                "LTV = Avg Transaction × Purchase Frequency × Avg Customer Lifespan\n"
                "```\n"
                "For one-time purchases: LTV = deal size.\n"
                "For repeat: factor in retention rate.\n\n"
                "### ROAS — Return on Ad Spend\n"
                "```\n"
                "ROAS = Revenue from Ads / Ad Spend\n"
                "```\n"
                "Target: 3:1 minimum for most businesses. 5:1+ is healthy.\n\n"
                "### The Golden Ratio\n"
                "**LTV:CAC should be at least 3:1.**\n"
                "- Below 1:1 → losing money on every client\n"
                "- 1:1 to 3:1 → unprofitable or breakeven after costs\n"
                "- 3:1 to 5:1 → healthy\n"
                "- Above 5:1 → you're underinvesting in growth (spend more!)"
            ),
            dynamic_prompt=(
                "Calculate unit economics for this client:\n\n"
                "- Estimated CAC based on {channel} + {Q44} budget + conversion rates\n"
                "- LTV based on {Q10} deal size + {Q11} repeat frequency + estimated lifespan\n"
                "- ROAS target based on margin ({Q22})\n\n"
                "Show the LTV:CAC ratio and interpret it:\n"
                "- If below 3:1: what needs to change (raise prices, improve conversion, reduce costs)\n"
                "- If above 5:1: 'you can afford to spend more on acquisition'\n\n"
                "If {Q11} = 'rarely' (one-time): LTV = deal size. State this and note that "
                "upsell/cross-sell could increase it (connect to U3 ascension model)."
            ),
        ),
        SectionSpec(
            name="Scaling Triggers & Kill Switch",
            purpose="When to double down and when to pivot",
            tone_note="Decisive. Specific thresholds, not 'when it feels right'.",
            static_content=(
                "## Decision Framework: Scale, Hold, or Kill\n\n"
                "### Scale Triggers (invest more)\n"
                "If ALL of these are true for 4+ consecutive weeks:\n"
                "- CAC is stable and below target\n"
                "- ROAS is above 3:1\n"
                "- You have capacity for more clients\n"
                "- Quality of leads/clients is acceptable\n"
                "→ **Increase ad spend by 20-30% per week. Monitor for 2 weeks.**\n\n"
                "### Hold Triggers (maintain and optimize)\n"
                "If numbers are close but not consistently hitting targets:\n"
                "→ **Don't increase spend. Optimize conversion, copy, targeting first.**\n\n"
                "### Kill Switch (stop and reassess)\n"
                "If after 8 weeks of consistent execution:\n"
                "- ROAS below 1:1 for 4+ weeks\n"
                "- CAC above 2× target with no improvement trend\n"
                "- Lead quality is consistently poor (>70% unqualified)\n"
                "→ **Pause spend. Reassess channel, targeting, offer, or landing page. "
                "Don't throw more money at a broken system.**"
            ),
            dynamic_prompt=(
                "Set specific scaling and kill-switch thresholds for this client.\n\n"
                "Using their numbers:\n"
                "- Target CAC: $X (from unit economics above)\n"
                "- Target ROAS: X:1\n"
                "- Budget: {Q44}\n"
                "- Capacity constraint: {Q43}\n\n"
                "Define:\n"
                "1. **Scale trigger**: 'If CAC < $X AND ROAS > X:1 for 4 weeks → increase to $Y/mo'\n"
                "2. **Hold trigger**: specific ranges\n"
                "3. **Kill switch**: specific thresholds and timeline\n"
                "4. **Pivot options**: if the primary channel doesn't work after 8 weeks, "
                "what's the recommended next channel? (from channel scoring)\n\n"
                "Be specific: '$X' not 'a reasonable amount'."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate the full financial analysis. "
                "All projections as HTML <table> elements with concrete numbers, not placeholders. "
                "Show both conservative and optimistic scenarios in side-by-side <table> rows."
            ),
        ),
        FormatSpec(
            format=Format.CHART,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate a Chart.js line chart config showing 6-month revenue projections.\n"
                "Two datasets: 'Conservative' and 'Optimistic'.\n"
                "Labels: Month 1 through Month 6.\n"
                "Include a horizontal dashed line for the revenue target.\n"
                "Return ONLY valid Chart.js JSON config."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q9", "Q10", "Q11",
        "Q15", "Q18", "Q19", "Q22",
        "Q27", "Q40", "Q41", "Q43", "Q44", "Q45",
    ],
    upstream_deps=[DocID.U1, DocID.U3, DocID.U4, DocID.U6],
    downstream_consumers=[DocID.U8, DocID.U9],
    maturity_adaptations={
        Maturity.STARTER: (
            "Focus on minimum viable investment and fastest path to first revenue. "
            "Break-even is the most important number. Keep projections modest — "
            "no hockey-stick charts for a pre-revenue business."
        ),
        Maturity.GROWING: (
            "Full model. Show how reinvestment accelerates growth. "
            "LTV:CAC is the key number to optimize."
        ),
        Maturity.ESTABLISHED: (
            "Optimization focus. Where is the marginal dollar best spent? "
            "Model scenarios: 'What if you increase price 20%?' vs 'What if you increase volume 20%?'"
        ),
        Maturity.PIVOT: (
            "New business financial reality check. How long can they fund the ramp-up? "
            "Include personal runway calculation."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.PRICING: (
            "Deep dive into how pricing changes cascade through the model. "
            "Show: 'At current price: X deals needed. At recommended price: Y deals needed.' "
            "Make the pricing change impact viscerally obvious."
        ),
        Bottleneck.VISIBILITY: "Standard depth. Focus on ad spend → lead → client waterfall.",
        Bottleneck.CONVERSION: "Model the impact of conversion rate improvements on total revenue.",
        Bottleneck.RETENTION: "Heavy emphasis on LTV. Show compounding retained revenue over 6 months.",
        Bottleneck.LEAD_GENERATION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Model revenue per client TYPE. Show that fewer, better clients = more profit.",
    },
    quality_rules=[
        "Every number must be traceable to an assumption. No magic numbers.",
        "Projections must have TWO scenarios minimum (conservative + optimistic).",
        "Conservative scenario must assume 50% of expected conversion rates, not 90%.",
        "Break-even must include ALL costs, including the client's time.",
        "Kill-switch criteria must be specific numbers, not 'if things aren't working'.",
        "If margin data is missing (Q22 = 'don't know'), note the gap and use 40% as default with a flag.",
        "ROAS targets must account for margin — a 3:1 ROAS at 20% margin means you're barely profitable.",
    ],
)