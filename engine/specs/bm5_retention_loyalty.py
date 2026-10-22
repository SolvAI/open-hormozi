# Fix the imports at the top of the file:

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec

BM5_SPEC = DocSpec(
    id=DocID.BM5,
    name="Retention, Loyalty & Referral Playbook",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Transform repeat purchase potential into a systematic retention engine. "
        "Design loyalty mechanics, referral incentives, and win-back sequences "
        "calibrated to the client's transaction frequency and deal size."
    ),
    sections=[
        SectionSpec(
            name="Retention Economics",
            purpose="Show the math: why keeping customers is cheaper than acquiring new ones",
            tone_note="STARTER: educational (they may not track LTV). ESTABLISHED: skip basics, show their specific numbers.",
            static_content=(
                "## Why Retention Is Your Highest-Leverage Investment\n\n"
                "- Acquiring a new customer costs 5-25× more than retaining one (HBR)\n"
                "- A 5% increase in retention = 25-95% increase in profit (Bain & Co)\n"
                "- Your best customers are the ones you already have\n\n"
                "### The Retention Equation\n"
                "Monthly Retained Revenue = Active Customers × Avg Transaction × Purchase Frequency\n"
                "Churn Rate = Customers Lost / Total Customers per period\n"
                "LTV = Avg Transaction × Purchase Frequency × Avg Customer Lifespan\n\n"
                "Before spending $1 on acquisition, ask: am I losing customers I already paid to acquire?"
            ),
            dynamic_prompt=(
                "Calculate this client's retention economics from their numbers: "
                "deal size ({Q10}), repeat frequency ({Q11}), current customers ({Q19}), "
                "current revenue ({Q18}). Estimate their current LTV and show how a "
                "10% improvement in retention frequency would impact monthly revenue. "
                "Be specific with their numbers, not generic."
            ),
        ),
        SectionSpec(
            name="Loyalty Program Design",
            purpose="Design the right loyalty mechanic for this business type",
            tone_note="Restaurant/retail: tangible rewards. Service: relationship-based. E-commerce: points/tiers.",
            static_content=(
                "## Loyalty Program Types\n\n"
                "| Type | Best For | Example |\n"
                "|------|----------|--------|\n"
                "| Punch card (buy X get 1 free) | High-frequency, low-ticket | Café, salon, car wash |\n"
                "| Points system | Medium frequency, medium ticket | Retail, e-commerce |\n"
                "| Tier system (bronze/silver/gold) | Aspirational, status-driven | Airlines, premium services |\n"
                "| Subscription/membership | Predictable revenue needed | Gym, SaaS, box service |\n"
                "| VIP access (exclusivity) | Premium positioning | Restaurant, consultant |\n\n"
                "### Design Rules\n"
                "1. Reward must be achievable within 2-3 purchases (or people give up)\n"
                "2. Reward value should be 5-15% of spend (enough to feel, not enough to kill margin)\n"
                "3. Make progress visible (stamps, points balance, tier status)\n"
                "4. Surprise bonuses > predictable rewards for emotional loyalty"
            ),
            dynamic_prompt=(
                "Recommend a specific loyalty program type for this client based on: "
                "business type ({Q1}), deal size ({Q10}), repeat frequency ({Q11}), "
                "margin ({Q22}). Design the specific mechanics: what's the reward, "
                "how many purchases to earn it, what does it cost the business, "
                "what's the projected ROI. "
                "If {Q1} = restaurant: design a concrete program (not just 'do a punch card'). "
                "If {Q1} = e-commerce: design with their product type in mind. "
                "Include the exact copy/wording for the loyalty offer."
            ),
        ),
        SectionSpec(
            name="Referral System",
            purpose="Turn happy customers into a predictable acquisition channel",
            tone_note="All profiles: referrals are free acquisition. Even CONSTRAINED resource profiles can do this.",
            static_content=(
                "## The Referral System Framework\n\n"
                "Most businesses 'hope' for referrals. A system PRODUCES them.\n\n"
                "### The 4 Components\n"
                "1. **Trigger**: WHEN to ask (peak satisfaction moment, not random)\n"
                "2. **Ask**: HOW to ask (specific script, not 'tell your friends')\n"
                "3. **Incentive**: WHAT they get (and what the referred friend gets)\n"
                "4. **Tracking**: HOW you know it's working (attribution)\n\n"
                "### When NOT to Ask\n"
                "- Before delivering value (they have nothing to refer)\n"
                "- When there's an unresolved complaint\n"
                "- Via mass blast ('refer a friend!' emails to everyone)\n\n"
                "### Double-Sided Incentives Win\n"
                "Give something to BOTH the referrer AND the new customer. "
                "This removes the social awkwardness of 'selling' to a friend."
            ),
            dynamic_prompt=(
                "Design a complete referral system for this client: "
                "1. Identify the peak satisfaction moment in their customer journey "
                "   (based on {Q7} what they deliver and {Q8} service vs product). "
                "2. Write the EXACT referral ask script/message (in their brand voice from U5). "
                "3. Design the incentive structure (calibrated to {Q10} deal size and {Q22} margin). "
                "4. Define tracking method appropriate to their tech level ({Q47}). "
                "If {Q23} already includes 'word of mouth': they have informal referrals. "
                "The system formalizes and amplifies what's already working."
            ),
        ),
        SectionSpec(
            name="Win-Back Strategy",
            purpose="Re-engage lapsed customers before they're gone forever",
            tone_note="SURVIVAL: this is urgent — reactivating lapsed customers is fastest revenue. Others: systematic.",
            static_content=(
                "## Win-Back Windows\n\n"
                "- **Warm lapsed** (1-2× expected purchase interval): gentle nudge\n"
                "- **Cold lapsed** (3-5×): re-engagement offer needed\n"
                "- **Lost** (>5×): hail mary with strongest offer, accept low response rate\n\n"
                "### Win-Back Sequence Structure\n"
                "1. 'We miss you' (emotional, no offer)\n"
                "2. 'Here's what's new' (value-add, soft offer)\n"
                "3. 'Special offer for returning customers' (incentive)\n"
                "4. 'Last chance' (urgency + best offer)\n"
                "5. 'Goodbye' (reverse psychology — surprisingly effective)"
            ),
            dynamic_prompt=(
                "Define lapsed thresholds for this business: "
                "based on {Q11} repeat frequency, what's the expected purchase interval? "
                "Set warm/cold/lost windows. "
                "Write the 5-email win-back sequence with actual copy, "
                "calibrated to their offer ({Q7}) and the reasons customers might lapse "
                "(derive from {Q36} and {Q37}). "
                "Include a reactivation offer — what discount/bonus/incentive makes sense "
                "given their margins ({Q22})?"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            prompt_fragment="Include all scripts and copy as <blockquote> blocks. Referral incentive as a <table>.",
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/bm5_loyalty_card.html",
            prompt_fragment=(
                "Generate the text content for a loyalty card / referral card. "
                "Return JSON: {\"card_type\": \"loyalty|referral\", \"headline\": \"...\", "
                "\"subline\": \"...\", \"reward\": \"...\", \"terms\": \"...\", \"brand_name\": \"...\"}"
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=["Q1", "Q7", "Q8", "Q10", "Q11", "Q18", "Q19", "Q22", "Q23", "Q36", "Q37", "Q47"],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Simple program. May not have enough customers yet for loyalty — focus on referral from early clients.",
        Maturity.GROWING: "Full loyalty + referral system. This is the scaling lever — systematize what's happening informally.",
        Maturity.ESTABLISHED: "Premium loyalty. VIP tiers. Formalize the ambassador program. Data-driven churn prediction.",
        Maturity.PIVOT: "Leverage old client relationships for referrals into new domain.",
    },
    bottleneck_adaptations={
        Bottleneck.RETENTION: "THIS IS THE PRIORITY DOC. Maximum depth on all sections. Win-back is urgent.",
        Bottleneck.VISIBILITY: "Light treatment — retention is secondary to being found.",
        Bottleneck.CONVERSION: "Moderate — if they close but don't retain, the funnel leaks at the bottom.",
        Bottleneck.PRICING: "Connect to U4 — retention may improve if pricing is restructured (subscriptions, bundles).",
    },
    quality_rules=[
        "Referral incentive must not exceed customer acquisition cost — or it defeats the purpose.",
        "Loyalty rewards must be funded from increased LTV, not eaten from existing margin.",
        "Win-back offers should NOT be available to active customers (perverse incentive to lapse).",
        "Every script must sound human, not corporate. A restaurant owner won't say 'leverage your network'.",
        "If the business has <10 customers, skip loyalty program and focus entirely on referral + win-back.",
    ],
)