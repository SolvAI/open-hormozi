"""U6: Sales Funnel Blueprint.

The complete customer journey from first touchpoint to repeat purchase,
assembled from the Channel (Tier 3) and Business Model (Tier 2) selections.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U6_SPEC = DocSpec(
    id=DocID.U6,
    name="Sales Funnel Blueprint",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Map the complete customer journey as a visual diagram and written walkthrough. "
        "Every step, decision node, and automation trigger from first awareness to "
        "repeat purchase. The funnel SHAPE is determined by Tier 2 + Tier 3 inputs."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Funnel Architecture Overview",
            purpose="Name the funnel shape and explain why it's right for this business",
            tone_note="Decisive. 'This is your funnel' not 'there are many options'.",
            static_content=(
                "## Common Funnel Shapes\n\n"
                "| Shape | Best For | Flow |\n"
                "|-------|----------|------|\n"
                "| **Direct Sales** | High-ticket B2B, consultative | Ad/Content → LP → Application → Call → Proposal → Close |\n"
                "| **Webinar** | Education-dependent, $2k+ | Ad/Content → Registration → Webinar → Application → Call → Close |\n"
                "| **Lead Magnet + Nurture** | Long buying cycle, trust-building | Ad/Content → Lead Magnet → Email Sequence → Call/Purchase |\n"
                "| **Self-Serve** | Low-ticket, e-commerce, SaaS | Ad/Content → Product Page → Cart → Purchase → Upsell |\n"
                "| **Local Discovery** | Physical location | Search/Maps/Social → Website/GBP → Visit/Reservation → Experience → Repeat |\n"
                "| **Marketplace Migration** | Currently marketplace-dependent | Marketplace → Great Work → Direct Relationship → Owned Channel |\n\n"
                "### Key Principles\n"
                "1. **Every step must have ONE clear next action** — no dead ends\n"
                "2. **Non-buyers get a second path** — not everyone buys on the first pass\n"
                "3. **Automation handles the predictable** — humans handle the nuanced\n"
                "4. **Measure every transition** — what you don't track, you can't improve"
            ),
            dynamic_prompt=(
                "Determine the funnel shape for this client based on:\n"
                "- Channel: {channel}\n"
                "- Conversation required: {Q13}\n"
                "- Appointment-based: {Q14}\n"
                "- Deal size: {Q10}\n"
                "- Sales cycle: {Q16}\n"
                "- Self-serve: {Q13}\n"
                "- Physical location: {Q6}\n"
                "- Offer type: {Q8}\n\n"
                "Name the funnel shape from the table above (or create a hybrid). "
                "Explain in 2-3 sentences why this shape fits THIS business. "
                "Briefly explain why other shapes were rejected."
            ),
        ),
        SectionSpec(
            name="Complete Funnel Diagram",
            purpose="Visual map of every step and decision node",
            tone_note="The diagram is the star of this section. The text explains what the diagram shows.",
            static_content=(
                "## Reading the Funnel Diagram\n\n"
                "- **Rectangles**: Steps the prospect takes\n"
                "- **Diamonds**: Decision points (qualified? bought? showed up?)\n"
                "- **Arrows**: Transitions (automated or manual)\n"
                "- **Dotted paths**: Secondary / nurture paths for non-buyers\n"
                "- **Labels on arrows**: What triggers the transition\n\n"
                "Every step has:\n"
                "1. An **owner** (automation, you, or your team)\n"
                "2. A **metric** (conversion rate at this step)\n"
                "3. A **tool** (what software handles this step)"
            ),
            dynamic_prompt=(
                "Describe the complete funnel for this client step-by-step.\n"
                "For each step include:\n"
                "1. **Step name** (e.g., 'Landing Page Visit')\n"
                "2. **What happens** (what the prospect experiences)\n"
                "3. **Decision branch** (what determines the next step)\n"
                "4. **Owner** (automated / human / tool)\n"
                "5. **Expected conversion %** (realistic for this industry/channel)\n\n"
                "Include BOTH paths:\n"
                "- **Main path**: awareness → interest → decision → purchase\n"
                "- **Secondary paths**: not-qualified → lead magnet → nurture → re-entry\n"
                "- **Post-purchase**: onboarding → delivery → retention → referral\n\n"
                "The Mermaid diagram format will visualize this — but the DOC format "
                "must contain the full written walkthrough with all details."
            ),
        ),
        SectionSpec(
            name="Automation Map",
            purpose="Specify which transitions are automated and with what tools",
            tone_note="Practical. Match automation complexity to MT3 tech comfort level.",
            static_content=(
                "## Automation Tiers\n\n"
                "| Level | What's Automated | Tools | Effort |\n"
                "|-------|-----------------|-------|--------|\n"
                "| **Level 1: Manual** | Nothing — you do everything by hand | Email, spreadsheet | 10+ hrs/week |\n"
                "| **Level 2: Basic** | Email reminders, form notifications | Calendly, Mailchimp | 3-5 hrs/week |\n"
                "| **Level 3: Connected** | Lead routing, follow-up sequences, CRM | Zapier/Make + CRM | 1-3 hrs/week |\n"
                "| **Level 4: Full** | Lead scoring, behavioral triggers, reporting | HubSpot, ActiveCampaign | <1 hr/week |\n\n"
                "**Start at Level 2.** Level 1 doesn't scale. Level 4 is overkill until $20k+/mo."
            ),
            dynamic_prompt=(
                "Design the automation map for this client's funnel.\n\n"
                "Match to their resources:\n"
                "- Tech comfort: {Q47}\n"
                "- Time available: {Q45}\n"
                "- Budget: {Q44}\n"
                "- Team size: {Q4}\n\n"
                "For each funnel step, specify:\n"
                "1. Manual or automated?\n"
                "2. If automated: what tool and what trigger\n"
                "3. What data is captured at this step\n"
                "4. What happens if the automation breaks (fallback)\n\n"
                "Recommend a specific automation level (1-4) with justification. "
                "If solo + limited tech: Level 2 max. Don't prescribe HubSpot to someone "
                "who can't build a landing page."
            ),
        ),
        SectionSpec(
            name="Conversion Benchmarks & Optimization Triggers",
            purpose="Set realistic expectations and define when to intervene",
            tone_note="Numbers-based. Show industry benchmarks alongside their specific targets.",
            static_content=(
                "## Funnel Conversion Benchmarks\n\n"
                "| Stage | B2B Service | B2C Local | E-commerce | SaaS |\n"
                "|-------|------------|-----------|------------|------|\n"
                "| Ad → LP visit | 2-5% CTR | 3-8% CTR | 1-3% CTR | 2-5% CTR |\n"
                "| LP → Lead | 10-25% | 5-15% | 2-4% | 5-15% |\n"
                "| Lead → Qualified | 30-50% | N/A | N/A | 20-40% |\n"
                "| Qualified → Call | 50-70% | N/A | N/A | N/A |\n"
                "| Call → Close | 20-40% | N/A | N/A | N/A |\n"
                "| Visit → Purchase | N/A | 30-60% | 2-4% | N/A |\n"
                "| Cart → Complete | N/A | N/A | 60-80% | N/A |\n\n"
                "### When to Optimize\n"
                "Fix the WORST-performing stage first. A 10% improvement at the worst "
                "stage beats a 50% improvement at the best stage.\n\n"
                "### The 80% Rule\n"
                "If any stage converts at less than 80% of the benchmark → that's your bottleneck."
            ),
            dynamic_prompt=(
                "Set specific conversion benchmarks for THIS client's funnel.\n\n"
                "Using the funnel steps defined above, set:\n"
                "1. **Target conversion rate** per step (realistic for their industry)\n"
                "2. **Minimum acceptable rate** (below this = action needed)\n"
                "3. **Optimization trigger**: what to try if below minimum\n"
                "4. **End-to-end conversion**: from first touch to purchase\n\n"
                "Calculate: 'If {channel} drives X visitors and each step converts at Y%, "
                "they'll get Z clients/mo → $W revenue.' Show the full waterfall.\n\n"
                "Connect to U7 (financial model) and U8 (KPI tracking)."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate the complete written funnel walkthrough. "
                "Each funnel step gets its own <h3> with all 5 details "
                "(step, what happens, decision, owner, conversion %). "
                "Include the benchmarks as an HTML <table>."
            ),
        ),
        FormatSpec(
            format=Format.MERMAID,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate a Mermaid flowchart TD diagram of the complete funnel.\n"
                "Use:\n"
                "- Rectangles for action steps: A[\"Step Name\"]\n"
                "- Diamonds for decisions: B{\"Qualified?\"}\n"
                "- Arrows with labels: A -->|\"trigger\"| B\n"
                "- Dotted lines for secondary paths: A -.->|\"not qualified\"| C\n"
                "- Subgraphs for funnel stages: subgraph \"Awareness\"\n\n"
                "Include ALL paths: main, secondary (nurture), and post-purchase.\n"
                "Quote ALL labels containing special characters.\n"
                "Maximum 25 nodes — consolidate sub-steps if needed for readability."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q6", "Q7", "Q8",
        "Q10", "Q13", "Q14", "Q15", "Q16",
        "Q44", "Q45", "Q47",
    ],
    upstream_deps=[DocID.U1, DocID.U2, DocID.U3, DocID.U4, DocID.U5],
    downstream_consumers=[DocID.U7, DocID.U8, DocID.U9],
    maturity_adaptations={
        Maturity.STARTER: (
            "Simpler funnel — fewer steps, fewer automations. "
            "'Get the first version working, then add complexity.' "
            "Max 6-8 steps. Level 2 automation."
        ),
        Maturity.GROWING: (
            "Full funnel with all paths. This is the document that systematizes "
            "what's currently ad-hoc. Level 2-3 automation."
        ),
        Maturity.ESTABLISHED: (
            "Optimization focus. They likely HAVE a funnel — redesign for efficiency. "
            "Level 3-4 automation. Include A/B testing nodes."
        ),
        Maturity.PIVOT: (
            "New funnel for new business, but leverage old domain contacts/reputation "
            "as a warm-start advantage."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Funnel emphasis on the awareness → interest transition. More detail on top-of-funnel.",
        Bottleneck.LEAD_GENERATION: "Funnel emphasis on interest → lead capture. Secondary paths are critical.",
        Bottleneck.CONVERSION: "Funnel emphasis on lead → sale. Extra decision nodes for objection handling.",
        Bottleneck.PRICING: "Standard depth. Funnel impact is mostly in the pricing presentation step.",
        Bottleneck.RETENTION: "Post-purchase funnel gets as much detail as the acquisition funnel.",
        Bottleneck.WRONG_CLIENTS: "Add explicit qualification / disqualification nodes early in the funnel.",
    },
    quality_rules=[
        "The Mermaid diagram must be renderable — no syntax errors, all labels quoted.",
        "Every funnel step must have an owner (who/what does this step).",
        "No dead ends — every node must have at least one outgoing path.",
        "Non-buyer paths must lead somewhere useful (nurture, not a void).",
        "Conversion estimates must be industry-appropriate, not generic '10%' everywhere.",
        "Automation recommendations must match the client's tech level from Q47.",
        "The funnel must match the channel — a local restaurant's funnel ≠ a SaaS funnel.",
    ],
)