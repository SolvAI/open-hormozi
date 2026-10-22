"""U4: Pricing & Packaging.

Restructure how the client charges to maximize revenue per client
while maintaining perceived fairness and conversion rate.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U4_SPEC = DocSpec(
    id=DocID.U4,
    name="Pricing & Packaging",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Design pricing architecture that captures the value defined in U3. "
        "Structure packages, payment terms, and anchoring logic that make "
        "the ideal tier feel like the obvious choice. Kill time-based pricing "
        "where it exists."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Current Pricing Diagnostic",
            purpose="Analyze what's broken or suboptimal in the current pricing model",
            tone_note="STARTER: educational, many haven't thought about pricing strategy. ESTABLISHED: straight to gaps.",
            static_content=(
                "## Pricing Is Not a Number — It's Architecture\n\n"
                "Most businesses set prices ONE of these ways (all wrong):\n"
                "1. **Cost-plus**: 'My costs + 30% margin' → ignores value\n"
                "2. **Competition-matching**: 'Others charge X, I charge X-10%' → race to bottom\n"
                "3. **Gut feel**: 'Feels about right' → leaving money on the table\n"
                "4. **Time-based**: 'X per hour/day' → punishes efficiency, caps income\n\n"
                "### The Right Way: Value-Based Pricing\n"
                "Price is a function of **perceived value to the buyer**, not your costs.\n"
                "Value = (Dream Outcome × Likelihood) / (Time × Effort)\n"
                "If you 10× the value, you can 3× the price and the buyer still wins.\n\n"
                "### Why Time-Based Pricing Is a Trap\n"
                "- It punishes you for getting faster and better\n"
                "- The client focuses on hours instead of outcomes\n"
                "- You can never scale beyond (hours × rate)\n"
                "- It commoditizes you: 'Why pay $800/day when Upwork has people at $400?'\n\n"
                "Transition: hourly/daily → project-based → value-based → retainer."
            ),
            dynamic_prompt=(
                "Diagnose this client's current pricing based on:\n"
                "- Current model: {Q9}\n"
                "- Average deal size: {Q10}\n"
                "- Monthly revenue: {Q18}\n"
                "- Margin: {Q22}\n"
                "- Structured offer: {Q12}\n"
                "- Engagement type: {Q15}\n\n"
                "Identify:\n"
                "1. What pricing model they're currently using and its specific problems\n"
                "2. Revenue left on the table (estimate based on {Q10} × {Q19} vs {Q18})\n"
                "3. The single biggest pricing lever for THIS business\n\n"
                "If {Q9} = hourly/daily: explain the transition path to project/value pricing "
                "with a concrete example using their service ({Q7}).\n"
                "If {Q9} = 'haven't formalized': build from scratch, not from fixing."
            ),
        ),
        SectionSpec(
            name="Package Architecture",
            purpose="Design the tier structure (or single-offer logic) with pricing",
            tone_note="LIFESTYLE: may only need 1 tier. GROWTH: full 3-tier. Local: menu/service list structure.",
            static_content=(
                "## Good / Better / Best (or Single-Offer Logic)\n\n"
                "### Three-Tier Architecture\n"
                "| Element | Good | Better | Best |\n"
                "|---------|------|--------|------|\n"
                "| **Purpose** | Entry point, filter tire-kickers | Core revenue driver | Premium, highest margin |\n"
                "| **% of buyers** | 10-20% | 60-70% | 10-20% |\n"
                "| **Pricing strategy** | Low enough to be a 'no-brainer' | Anchored between Good and Best | 3-5× Good |\n"
                "| **What's included** | Core deliverable only | Core + key bonuses | Everything + exclusivity |\n\n"
                "### When to Use Single-Offer\n"
                "- You're pre-revenue and need to validate ONE thing\n"
                "- Your capacity is so limited that tiers create complexity you can't handle\n"
                "- You're premium-only and tiers would dilute the brand\n\n"
                "### The Decoy Effect\n"
                "The 'Good' tier exists to make 'Better' look like a bargain. "
                "Price Good at 60-70% of Better with 30% of the value → Better becomes obvious.\n\n"
                "### Anchoring Rules\n"
                "1. Always show the most expensive option first (even if few buy it)\n"
                "2. The middle tier should be the one you WANT them to buy\n"
                "3. Name tiers after outcomes, not levels (not 'Bronze/Silver/Gold')"
            ),
            dynamic_prompt=(
                "Design the package architecture for this client.\n\n"
                "Inputs from U3 (upstream): value stack, offer structure, ascension model.\n"
                "Current situation: {Q10} deal size, {Q12} offer structure, {Q9} pricing model.\n"
                "Target: {Q40} monthly revenue with {Q43} ideal capacity.\n\n"
                "Design:\n"
                "1. **Tier structure** (single, 2-tier, or 3-tier) with rationale\n"
                "2. **Price point per tier** with anchoring math\n"
                "   (Show: 'If target = ${Q40}/mo and capacity = X clients, "
                "   then average deal must be $Y')\n"
                "3. **Package comparison table**: what's in each tier, what's excluded\n"
                "4. **Tier names** using MAGIC naming from U3\n\n"
                "If {Q1} = restaurant: packages = menu formulas (lunch, dinner, events). "
                "Not 'Good/Better/Best' — adapt the structure to the business.\n"
                "If {Q1} = e-commerce: packages = product bundles, subscription tiers.\n"
                "If {Q8} = physical product: pricing is per-unit + upsell logic, not service tiers."
            ),
        ),
        SectionSpec(
            name="Payment Terms & Negotiation Rules",
            purpose="Remove friction from the payment process and protect margins",
            tone_note="Direct. These are RULES, not suggestions. 'Never discount, add bonuses.'",
            static_content=(
                "## Payment Terms\n\n"
                "### For Services ($2k+)\n"
                "- **Deposit**: 30-50% upfront, non-refundable. Covers your risk.\n"
                "- **Milestones**: Remaining split across 1-3 milestones tied to deliverables.\n"
                "- **Net terms**: Net 15 for B2B (never Net 60 — you're not a bank).\n"
                "- **Late payment**: Include late payment penalties per applicable commercial law "
                "(e.g., statutory interest rates + fixed recovery fees where permitted).\n\n"
                "### For Products / Low Ticket\n"
                "- Payment at purchase. No invoicing.\n"
                "- Split payment (2-3x installments) for $500+.\n\n"
                "### The Hormozi Negotiation Rule\n"
                "**Never discount. Add bonuses.**\n"
                "- Client asks for 20% off → add a bonus worth 20% of the price instead\n"
                "- Discounting trains clients to always ask for less\n"
                "- Bonuses increase perceived value; discounts decrease it\n\n"
                "### Minimum Engagement\n"
                "If you offer retainers/subscriptions: minimum 3-month commitment. "
                "It takes 30-60 days for results to show. Allowing monthly cancellation "
                "means clients leave before the value materializes."
            ),
            dynamic_prompt=(
                "Design payment terms for this client:\n"
                "- Deal size: {Q10}\n"
                "- Engagement type: {Q15}\n"
                "- Business type: {Q1}\n"
                "- Offer type: {Q8}\n\n"
                "Include:\n"
                "1. **Deposit structure** (amount, timing, refundability)\n"
                "2. **Payment schedule** for the designed packages\n"
                "3. **3 specific negotiation responses** for common discount requests "
                "('Can you do it for less?', 'Our budget is only X', 'Competitor quoted Y')\n"
                "4. **Minimum engagement** if applicable\n"
                "5. **Price increase triggers**: conditions under which to raise prices "
                "(e.g., 'when you're at 80% capacity', 'after 10 completed projects', "
                "'every January 1st')\n\n"
                "If {Q10} < $500: keep it simple — payment at purchase, maybe 2x split.\n"
                "If {Q10} > $5k: full deposit + milestone structure with contract terms."
            ),
        ),
        SectionSpec(
            name="Revenue Math & Price Validation",
            purpose="Prove the pricing hits the revenue target with capacity constraints",
            tone_note="Numbers-driven. This is the bridge between U4 and U7.",
            static_content=(
                "## The Revenue Equation\n\n"
                "```\n"
                "Monthly Revenue = Clients/month × Average Deal Size × Purchase Frequency\n"
                "```\n\n"
                "Your pricing must satisfy this equation given your capacity constraints.\n"
                "If the math doesn't work, you need to either:\n"
                "1. **Raise prices** (most common fix)\n"
                "2. **Increase frequency** (retention/upsell)\n"
                "3. **Increase capacity** (hire, automate)\n"
                "4. **Change model** (1:many, productize, subscription)\n\n"
                "### Price Increase Signal Checklist\n"
                "✅ You haven't raised prices in 12+ months\n"
                "✅ No one pushes back on price\n"
                "✅ You're above 80% capacity\n"
                "✅ Your close rate is above 60%\n"
                "✅ Clients say 'that's surprisingly reasonable'\n"
                "If 3+ are true: you're undercharging."
            ),
            dynamic_prompt=(
                "Run the revenue math for this client:\n\n"
                "Given:\n"
                "- Target: {Q40}/mo\n"
                "- Current: {Q18}/mo\n"
                "- Current deal size: {Q10}\n"
                "- Current clients/mo: {Q19}\n"
                "- Ideal capacity: {Q43}\n"
                "- Margin: {Q22}\n\n"
                "Calculate:\n"
                "1. Deals needed per month at CURRENT price to hit target\n"
                "2. Deals needed per month at RECOMMENDED price to hit target\n"
                "3. Gap analysis: what has to change (price, volume, or both)\n"
                "4. Price increase signal checklist: evaluate each for this client\n\n"
                "Present as a simple table:\n"
                "| Scenario | Deal Size | Deals/Mo | Revenue | Feasible? |\n"
                "Show 3 scenarios: current pricing, moderate increase, ideal pricing.\n\n"
                "If the math reveals they need 50 clients/mo as a solo consultant → "
                "flag that pricing MUST increase. Make the impossibility obvious."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Package comparison table must be "
                "formatted as a clean html table. Revenue math must use concrete numbers."
            ),
        ),
        FormatSpec(
            format=Format.XLS,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            template_path="templates/excel/u4_pricing_calculator.xlsx",
            prompt_fragment=(
                "Generate JSON to fill the pricing calculator template.\n"
                "Return ONLY valid JSON with this exact structure:\n"
                "```json\n"
                "{\n"
                '  "row_injections": [\n'
                '    {\n'
                '      "sheet": "Pricing Tiers",\n'
                '      "start_row": 2,\n'
                '      "rows": [\n'
                '        ["Tier 1 Name", "Description", price_number, anchor_price_number, null, delivery_cost_number, null, null, "Yes/No"],\n'
                '        ["Tier 2 Name", "Description", price_number, anchor_price_number, null, delivery_cost_number, null, null, "Yes/No"],\n'
                '        ["Tier 3 Name", "Description", price_number, anchor_price_number, null, delivery_cost_number, null, null, "Yes/No"]\n'
                '      ]\n'
                '    },\n'
                '    {\n'
                '      "sheet": "LTV Calculator",\n'
                '      "start_row": 1,\n'
                '      "rows": [\n'
                '        [null, avg_transaction_value],\n'
                '        [null, purchase_frequency_per_year],\n'
                '        [null, avg_customer_lifespan_years],\n'
                '        [null, null],\n'
                '        [null, null],\n'
                '        [null, estimated_cac]\n'
                '      ]\n'
                '    },\n'
                '    {\n'
                '      "sheet": "Break-Even",\n'
                '      "start_row": 2,\n'
                '      "rows": [\n'
                '        [null, monthly_fixed_costs],\n'
                '        [null, avg_deal_size],\n'
                '        [null, variable_cost_per_deal]\n'
                '      ]\n'
                '    }\n'
                '  ]\n'
                "}\n"
                "```\n\n"
                "Rules:\n"
                "- Use `null` for formula cells (columns 5,7,8 in Pricing Tiers, and calculated rows in LTV/Break-Even) — formulas are already in the template.\n"
                "- Use `null` for column A labels in LTV Calculator and Break-Even — labels are already in the template.\n"
                "- All prices/costs as raw numbers (no currency symbols, no formatting).\n"
                "- Derive values from the U3 offer design and U4 pricing analysis above.\n"
                "- For Pricing Tiers: fill 2-4 rows depending on how many tiers were recommended.\n"
                "- For LTV Calculator: estimate purchase frequency and lifespan from {Q11} and {Q15}.\n"
                "- For Break-Even: estimate fixed costs from the investment breakdown in U7 context.\n"
                "- CAC estimate from channel cost analysis."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM,    
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate an HTML+CSS pricing comparison card for screenshotting at 1200×800px.\n"
                "Show 2-3 pricing tiers side by side as cards.\n"
                "The recommended tier should be visually highlighted (border, badge, background).\n"
                "Each card: tier name, price, period, short description, feature list, CTA button.\n"
                "Use fixed dimensions, clean modern design, professional typography.\n"
                "All content must be filled with this client's actual pricing — no placeholders."
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12",
        "Q15", "Q18", "Q19", "Q22",
        "Q40", "Q43",
    ],
    upstream_deps=[DocID.U1, DocID.U2, DocID.U3],
    downstream_consumers=[DocID.U6, DocID.U7, DocID.BM1, DocID.FC1, DocID.FC3],
    maturity_adaptations={
        Maturity.STARTER: (
            "Start simple. One or two tiers max. Don't over-engineer pricing before "
            "validating demand. Emphasis on 'set a real price and test it' over perfecting tiers."
        ),
        Maturity.GROWING: (
            "Restructure for value. Kill hourly/daily if present. "
            "Introduce proper tiering to increase average deal size."
        ),
        Maturity.ESTABLISHED: (
            "Optimize and raise. Client likely undercharges relative to proof. "
            "Introduce premium tier. Analyze which tier drives most profit (not just revenue)."
        ),
        Maturity.PIVOT: (
            "Bridge pricing: can charge more than a true beginner because of transferable "
            "expertise, but less than in old domain until new proof exists."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.PRICING: (
            "THIS IS THE PRIORITY DOC. Maximum depth on all sections. "
            "The revenue math section must be crystal clear — show them they're undercharging. "
            "Include specific 'raise your price by X%' recommendation with supporting logic."
        ),
        Bottleneck.VISIBILITY: "Standard depth — pricing is secondary to being found.",
        Bottleneck.CONVERSION: "Pricing may be part of the conversion problem. Check if price is a stated objection.",
        Bottleneck.RETENTION: "Focus on recurring pricing models (subscription, retainer, loyalty pricing).",
        Bottleneck.LEAD_GENERATION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Pricing as a FILTER. High prices repel wrong clients. Design accordingly.",
    },
    quality_rules=[
        "Price recommendations must be backed by math, not feelings.",
        "Package comparison table must be scannable in 5 seconds — which tier is best for whom.",
        "Never recommend a price without showing how many deals are needed to hit the revenue target.",
        "If transitioning from time-based: show a concrete before/after example with their real numbers.",
        "Payment terms must reference applicable commercial law where relevant.",
        "Negotiation responses must sound natural, not like a sales training manual.",
        "If restaurant or retail: 'packages' = menu formulas, product bundles — adapt language to context.",
    ],
)