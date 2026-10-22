from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U3_SPEC = DocSpec(
    id=DocID.U3,
    name="Grand Slam Offer",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Design the core offer using Hormozi's Value Equation. "
        "Restructure what the client sells into a stack that maximizes "
        "perceived value while including legal guardrails on claims."
    ),
    model_tier=ModelTier.MAX,  # core strategic doc — needs best model
    sections=[
        SectionSpec(
            name="Value Equation Diagnostic",
            purpose="Score the current offer on the 4 Value Equation dimensions",
            tone_note="STARTER: educational, explain the framework. ESTABLISHED: skip theory, go straight to gaps.",
            static_content=(
                "## The Value Equation\n\n"
                "Value = (Dream Outcome × Perceived Likelihood of Achievement) / "
                "(Time Delay × Effort & Sacrifice)\n\n"
                "To increase value, you either increase the numerator or decrease the denominator. "
                "Most businesses only work on Dream Outcome. The real leverage is in the other three.\n\n"
                "### The 4 Dimensions\n\n"
                "| Dimension | To Increase Value… | Example Lever |\n"
                "|-----------|-------------------|---------------|\n"
                "| **Dream Outcome** | Make the promised result bigger, more specific | 'Get clients' → 'Get 5 qualified leads/week within 30 days' |\n"
                "| **Perceived Likelihood** | Add proof, remove risk, add guarantee | Case studies, conditional guarantee, credentials |\n"
                "| **Time Delay** | Shorten time to first result | Quick-win in week 1, faster onboarding, instant access |\n"
                "| **Effort & Sacrifice** | Reduce what the buyer must do/give up | Done-for-you vs DIY, fewer meetings, no tech skills needed |\n\n"
                "### Self-Assessment Questions\n"
                "- What effort does your client need to expend to get the result?\n"
                "- How long between payment and first tangible result?\n"
                "- What makes them doubt it will work for *them* specifically?\n"
                "- Is your dream outcome stated in *their* words or *your* jargon?\n"
                "- What do they have to sacrifice (time, other options, comfort) to work with you?"
            ),
            dynamic_prompt=(
                "Based on the client's offer ({Q7}), target audience ({Q34}), "
                "and the problem they solve ({Q35}), score each of the 4 Value Equation "
                "dimensions 1-10 and explain WHY with specific evidence from their answers. "
                "Then provide 2-3 concrete actions to improve each dimension for THIS business.\n\n"
                "For the score summary, title it 'YOUR CURRENT SCORE' and anchor each score:\n"
                "- DREAM OUTCOME (0: vague promise no one gets excited about · 10: specific, measurable result in the buyer's own words)\n"
                "- PERCEIVED LIKELIHOOD (0: no proof, buyer assumes it won't work · 10: overwhelming evidence it works for people like them)\n"
                "- TIME DELAY (0: months before any visible result · 10: first tangible win within days)\n"
                "- EFFORT & SACRIFICE (0: buyer does all the work and figures it out alone · 10: done-for-them, zero friction)\n\n"
                "Current alternatives ({Q37}) reveal what the buyer considers 'normal' — "
                "use this to show where the client's offer already beats alternatives and where it doesn't.\n\n"
                "If {Q12} shows no structured offer, the score will likely be low on Perceived Likelihood "
                "(no clear promise) and high on Effort (buyer has to figure out what they're getting)."
            ),
        ),
        SectionSpec(
            name="Value Stack Design",
            purpose="Build the core offer + bonuses + naming",
            tone_note="STARTER: simpler stack, 1-2 bonuses max. ESTABLISHED: full stack with premium tier.",
            static_content=(
                "## Stack Architecture Rules\n\n"
                "1. The **core deliverable** solves the stated problem directly\n"
                "2. Each **bonus** removes a specific obstacle to the buyer's success\n"
                "3. **Name** each component using the MAGIC framework:\n"
                "   - **M**agnet word (power verb: Accelerator, Blueprint, Vault…)\n"
                "   - **A**vatar (who it's for)\n"
                "   - **G**oal (what they achieve)\n"
                "   - **I**nterval (in what timeframe)\n"
                "   - **C**ontainer (format: system, toolkit, session…)\n"
                "4. Never discount — add bonuses instead\n"
                "5. Each bonus must have a **believable standalone price** "
                "(ask: 'would someone pay this for just this piece?')\n"
                "6. Order the stack: core first, then bonuses from most to least impactful\n"
                "7. Total anchored value should be 3-10× the asking price\n\n"
                "### Common Bonus Types\n"
                "- **Speed bonus**: gets them the result faster (templates, swipe files, done-for-you setup)\n"
                "- **Risk-reversal bonus**: reduces their fear (extra support, check-in calls, guarantee extension)\n"
                "- **Ease bonus**: reduces their effort (automation, checklists, concierge onboarding)\n"
                "- **Exclusivity bonus**: makes them feel special (community access, direct line, priority)"
            ),
            dynamic_prompt=(
                "Design a value stack for this client's offer.\n\n"
                "**Core offer** based on {Q7}.\n"
                "**Bonuses** derived from:\n"
                "- Obstacles their audience faces: {Q36} (consequences of inaction = pains to solve with bonuses)\n"
                "- What alternatives offer: {Q37} (gaps in alternatives = bonus opportunities)\n"
                "- Buyer effort required: what does the client currently ask the buyer to do? Reduce it.\n\n"
                "Apply MAGIC naming to every component.\n"
                "Include 'believable' price anchoring for each (based on {Q10} deal size as reference — "
                "bonuses should be priced relative to what the buyer already considers reasonable).\n\n"
                "If {Q12} = 'no structure' or 'quote case by case': build the stack from scratch. "
                "Explain why packaging beats custom quoting.\n"
                "If {Q12} = 'clear packages': restructure and improve what exists. Don't throw it away."
            ),
        ),
        SectionSpec(
            name="Guarantee Design",
            purpose="Design the right guarantee type with legal framing",
            tone_note="If Q32=weak/none: softer guarantee with conditions. If strong proof: bold guarantee.",
            static_content=(
                "## Guarantee Types\n\n"
                "| Type | Risk Level | Best When | Example |\n"
                "|------|-----------|-----------|--------|\n"
                "| **Unconditional** | Highest (for you) | Strong proof, high confidence in delivery | 'Full refund within 30 days, no questions asked' |\n"
                "| **Conditional** | Moderate | You can define clear success criteria | 'Full refund if you complete all modules and don't see X result' |\n"
                "| **Anti-guarantee** | Low | Premium positioning, filtering buyers | 'This is NOT for people who won't do the work' |\n"
                "| **Performance** | Variable | Measurable outcomes exist | 'If we don't generate X leads in 90 days, we work free until we do' |\n"
                "| **Milestone** | Low | Long engagements | 'Review at day 30 — if not on track, full refund of remaining' |\n\n"
                "### Legal Guardrails\n"
                "- **Professional diligence ≠ guaranteed outcomes.** Frame guarantees as commitment "
                "to best-effort professional delivery, not guaranteed specific results. "
                "This is critical for service businesses in any jurisdiction.\n"
                "- Any income/result claim must include a **'results not typical'** disclaimer.\n"
                "- **Terms of sale** must spell out: guarantee terms, exclusions, refund process, timeline.\n"
                "- Many jurisdictions have a **cooling-off period** for distance/online sales "
                "(e.g., 14 days in the EU, 3 days for certain US contracts). "
                "This is a LEGAL RIGHT separate from your marketing guarantee.\n"
                "- For services begun before the cooling-off period ends, you may charge pro-rata "
                "for work delivered IF the client explicitly waived the waiting period in writing.\n\n"
                "### Guarantee Psychology\n"
                "A strong guarantee INCREASES conversion more than it increases refunds. "
                "Most people don't refund — they just needed the safety net to say yes. "
                "If your refund rate exceeds 10%, the problem is your delivery, not your guarantee."
            ),
            dynamic_prompt=(
                "Recommend the best guarantee type for this client based on:\n"
                "- Proof level: {Q32}\n"
                "- Deal size: {Q10} (higher = more guarantee needed to reduce risk)\n"
                "- Service vs product: {Q8}\n"
                "- Maturity: {maturity_profile}\n\n"
                "Write the **actual guarantee copy** they can use — not a description, the real text.\n"
                "Include the legal framing (professional diligence language, terms of sale notes).\n\n"
                "If proof is weak: recommend conditional over unconditional. "
                "Explain what conditions to set and why.\n"
                "If proof is strong: recommend bolder guarantee. "
                "Show how their existing results ({Q33} if available) back it up.\n\n"
                "If {Q8} = physical product: guarantee focuses on satisfaction + return logistics.\n"
                "If {Q8} = service: guarantee focuses on process commitment + milestone reviews."
            ),
        ),
        SectionSpec(
            name="Scarcity & Urgency Levers",
            purpose="Design ethical scarcity/urgency mechanisms",
            tone_note="All profiles: only use REAL scarcity. Fake urgency destroys trust.",
            static_content=(
                "## Ethical Scarcity & Urgency\n\n"
                "Scarcity and urgency work — but only when **real**. Fake countdown timers and "
                "'only 3 spots left' (that never runs out) erode trust permanently.\n\n"
                "### Real Scarcity Sources\n"
                "- **Capacity**: you can only take X clients/month (real if you're a service provider)\n"
                "- **Cohort**: next group starts on [date], enrollment closes [date] (real if you run cohorts)\n"
                "- **Seasonal**: price increases on [date] (real if you commit to it publicly)\n"
                "- **Bonus window**: bonuses available until [date], then core offer only\n"
                "- **Inventory**: limited stock (real for physical products)\n\n"
                "### What NOT to Do\n"
                "- Fake countdown timers that reset\n"
                "- 'Only X spots left' that never changes\n"
                "- Manufactured urgency with no real deadline\n"
                "- Pressure tactics that make the buyer feel manipulated"
            ),
            dynamic_prompt=(
                "Design 1-2 scarcity/urgency mechanisms for this client that are **genuinely real**.\n"
                "Based on:\n"
                "- Business type: {Q1} (a solo consultant has REAL capacity limits; an e-commerce store doesn't)\n"
                "- Offer type: {Q8}\n"
                "- Ideal week: {Q43} (reveals real capacity constraints)\n"
                "- Deal size: {Q10} (higher ticket = more justified urgency)\n\n"
                "If the business has no natural scarcity (e.g., digital product with unlimited inventory), "
                "recommend bonus-window urgency or cohort model instead of fake limits.\n"
                "Write the actual urgency copy they can use."
            ),
        ),
        SectionSpec(
            name="Ascension Model",
            purpose="Map entry → core → premium path",
            tone_note="LIFESTYLE: may only need 1 tier. GROWTH: full 3-tier. SURVIVAL: skip, focus on one offer.",
            static_content=(
                "## The Ascension Ladder\n\n"
                "Not every client needs the same thing. An ascension model gives buyers a natural path "
                "from first purchase to premium engagement:\n\n"
                "```\n"
                "ENTRY (low risk, low price)  →  CORE (main offer)  →  PREMIUM (highest value)\n"
                "```\n\n"
                "### Design Principles\n"
                "- **Entry** must deliver a genuine quick win (not a teaser that frustrates)\n"
                "- **Core** is your bread and butter — most revenue comes from here\n"
                "- **Premium** is for clients who want more: done-for-you, ongoing, exclusive\n"
                "- Each step should feel like the **obvious** next move after the previous one\n"
                "- Price gaps between tiers: typically 3-5× (entry $X → core $3-5X → premium $10-20X)\n\n"
                "### When NOT to Build an Ascension Model\n"
                "- You're pre-revenue: sell ONE thing first. Validate before expanding.\n"
                "- You want lifestyle: one focused offer at premium price serves you better.\n"
                "- Your capacity is maxed: adding tiers adds complexity you can't handle."
            ),
            dynamic_prompt=(
                "Design an ascension path for this client.\n\n"
                "- Entry point calibrated to {Q10} current deal size "
                "(or lower if entry should be a smaller commitment)\n"
                "- Core offer = the Grand Slam Offer designed above\n"
                "- Premium tier aimed at the capacity/revenue described in {Q43}\n\n"
                "If {ambition_profile} = LIFESTYLE: recommend a single focused offer. "
                "Explain why simplicity serves their goals better than tiers.\n"
                "If {ambition_profile} = SURVIVAL: skip ascension entirely. "
                "Focus on the ONE offer that generates revenue fastest. "
                "They can build tiers later.\n"
                "If {Q15} = ongoing/retainer: premium tier should be the retainer. "
                "Entry = project, core = larger project, premium = ongoing retainer.\n"
                "If {Q11} = repeat purchase: ascension can be frequency-based "
                "(single purchase → bundle → subscription)."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment="Use <h2> and <h3> for section hierarchy. Format the value stack as an HTML <table>.",
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.STATIC,
            template_path="templates/static_assets/u3_value_stack.png",
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q10", "Q11", "Q12",
        "Q15", "Q32", "Q33", "Q34", "Q35", "Q36",
        "Q37", "Q40", "Q43",
    ],
    upstream_deps=[DocID.U1, DocID.U2],
    downstream_consumers=[DocID.U4, DocID.U5, DocID.U6, DocID.BM1, DocID.FC1, DocID.FC3],
    maturity_adaptations={
        Maturity.STARTER: (
            "Simpler offer structure. 1-2 bonuses max, not a complex stack. "
            "Lower entry price point. Proof generation is critical — softer guarantees. "
            "More educational tone: explain WHY each element matters."
        ),
        Maturity.GROWING: (
            "Restructure existing offer for value. Kill hourly/daily rates if present (Q9). "
            "Push toward packages. Client likely has an informal offer that needs formalizing."
        ),
        Maturity.ESTABLISHED: (
            "Premium positioning. Bold guarantees backed by proof. "
            "Full ascension model with clear premium tier. "
            "Client has authority — the offer should reflect it."
        ),
        Maturity.PIVOT: (
            "Bridge old domain credibility into new offer. "
            "'X years doing Y, now applying that expertise to Z.' "
            "Guarantee can lean on track record even if new domain proof is thin."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Standard depth — offer is secondary to being seen.",
        Bottleneck.LEAD_GENERATION: "Standard depth. Offer matters but isn't the bottleneck.",
        Bottleneck.CONVERSION: (
            "DEEP — offer is likely the core problem. "
            "Extra attention to guarantee design, objection preemption in the stack, "
            "and reducing perceived risk. If leads exist but don't convert, the offer isn't compelling enough."
        ),
        Bottleneck.PRICING: (
            "DEEP — this is the priority document. Full restructure of how value is packaged and priced. "
            "Kill time-based pricing. Build value stack that justifies 2-3× current price."
        ),
        Bottleneck.RETENTION: (
            "Focus ascension model on keeping existing clients buying more. "
            "Core offer may be fine — add premium/ongoing tier."
        ),
        Bottleneck.WRONG_CLIENTS: (
            "Redesign offer for the RIGHT audience, not the current one. "
            "Stack should repel wrong-fit clients and attract ideal ones."
        ),
    },
    quality_rules=[
        "Never promise specific financial results without 'results not typical' framing.",
        "Always distinguish professional diligence from guaranteed outcomes.",
        "Bonuses must be genuinely useful, not filler padding.",
        "If the client sells a service, the offer must reduce perceived effort/sacrifice for the BUYER, not describe the seller's process.",
        "Price anchoring must be believable — don't claim a PDF checklist is 'worth $2,000'.",
        "The MAGIC naming framework should produce names that sound natural and professional — not forced marketing jargon.",
        "If the client's current pricing is time-based (Q9 = hourly/daily), explicitly address WHY and HOW to transition to value-based.",
        "Scarcity mechanisms must be genuinely real. If the business has no natural scarcity, say so.",
    ],
)