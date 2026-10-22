"""CH6: Referral & Partnership Strategy.

Systematize word-of-mouth and build strategic partnerships
as a primary acquisition channel.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH6_SPEC = DocSpec(
    id=DocID.CH6,
    name="Referral & Partnership Strategy",
    tier=Tier.CHANNEL,
    purpose=(
        "Transform informal word-of-mouth into a systematic referral and partnership engine. "
        "Ideal partner profiles, incentive structures, outreach scripts, "
        "co-marketing opportunities, and referral tracking."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Referral System Design",
            purpose="Turn happy clients into predictable referral sources",
            tone_note="If they already get WOM referrals, the system formalizes what works. Don't fix what isn't broken.",
            static_content=(
                "## From Random to Systematic\n\n"
                "Most businesses 'get referrals sometimes.' A system PRODUCES them reliably.\n\n"
                "### The Referral Math\n"
                "If 30% of happy clients refer when asked (typical), and you ask 10 clients/month:\n"
                "→ 3 referrals/month. At 50% conversion: 1.5 new clients/month. For free.\n\n"
                "### The 3 Referral Types\n"
                "| Type | How It Works | Best For |\n"
                "|------|-------------|----------|\n"
                "| **Passive** | You do great work, they mention you | Existing default |\n"
                "| **Active ask** | You ask directly at the right moment | Most businesses |\n"
                "| **Incentivized** | You give something for each referral | Repeat purchase businesses |\n\n"
                "### When to Ask\n"
                "The ask must happen at PEAK SATISFACTION — not randomly.\n"
                "- Right after a compliment\n"
                "- Right after delivering a big result\n"
                "- Right after a positive review\n"
                "- Right after a contract renewal"
            ),
            dynamic_prompt=(
                "Design the referral system for this client.\n\n"
                "Based on:\n"
                "- Current WOM: {Q23}, {Q24}\n"
                "- Client volume: {Q19}\n"
                "- Deal size: {Q10}\n"
                "- Repeat potential: {Q11}\n"
                "- Margin: {Q22}\n\n"
                "Produce:\n"
                "1. **Referral type** recommendation (passive / active / incentivized) with rationale\n"
                "2. **Peak satisfaction moments** specific to their service ({Q7})\n"
                "3. **Ask scripts**: verbal, email, SMS (full copy)\n"
                "4. **Incentive structure** (if applicable): what the referrer gets, "
                "what the referred gets, cost to the business\n"
                "5. **Monthly referral target** based on current client volume\n"
                "6. **Tracking method** appropriate to their tech level ({Q47})\n\n"
                "If {Q24} = 'word of mouth': they already have organic referrals. "
                "The system amplifies 2-3x what's already happening."
            ),
        ),
        SectionSpec(
            name="Strategic Partnerships",
            purpose="Identify and activate complementary businesses for mutual referrals",
            tone_note="Partnerships are the second engine. Different from individual referrals.",
            static_content=(
                "## The Partnership Model\n\n"
                "### Ideal Partner Criteria\n"
                "A good partner:\n"
                "1. Serves the SAME customer but with a DIFFERENT service\n"
                "2. Has a complementary (not competing) offer\n"
                "3. Has access to your audience at a different stage\n"
                "4. Is roughly your size (or slightly larger)\n\n"
                "### Partnership Types\n"
                "| Type | Effort | Impact | Example |\n"
                "|------|--------|--------|--------|\n"
                "| **Mutual referral** | Low | Medium | 'I send you my overflow, you send me yours' |\n"
                "| **Co-marketing** | Medium | High | Joint webinar, co-authored content |\n"
                "| **Bundle** | Medium | High | Package your service with theirs |\n"
                "| **Affiliate/commission** | Low | Variable | % for each referral that converts |\n"
                "| **White-label** | High | High | They resell your service under their brand |\n\n"
                "### The Partnership Pitch\n"
                "Lead with THEIR benefit, not yours.\n"
                "❌ 'I'd love to partner with you to get more clients.'\n"
                "✅ 'Your clients probably need [X]. I can handle that, so you don't have to. "
                "And I'll send my clients to you for [Y].'"
            ),
            dynamic_prompt=(
                "Build the partnership strategy for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Industry: {Q2}\n"
                "- Service: {Q7}\n"
                "- Target customer: {Q34}\n"
                "- Location: {Q5}\n\n"
                "Produce:\n"
                "1. **5 ideal partner profiles** (specific business types, not generic)\n"
                "   Example: not 'marketing agency' but 'brand designer for startups who "
                "   doesn't do development'\n"
                "2. **Partnership type** per profile (mutual referral, co-marketing, etc.)\n"
                "3. **Outreach script** (email or DM — full copy)\n"
                "4. **Partnership proposal outline** (1-page: what you offer, what you ask, terms)\n"
                "5. **Co-marketing idea** per partner (specific joint activity)\n"
                "6. **Tracking**: how to attribute partner referrals"
            ),
        ),
        SectionSpec(
            name="Activation & Tracking",
            purpose="Make the system operational — who does what, when, and how to measure",
            tone_note="Turn strategy into weekly actions. Not a plan that sits in a drawer.",
            static_content=(
                "## Making It Operational\n\n"
                "### Weekly Referral Routine (30 min/week)\n"
                "1. Identify 2-3 clients at peak satisfaction this week\n"
                "2. Send the referral ask (script from above)\n"
                "3. Follow up on pending referral conversations\n"
                "4. Thank anyone who referred (handwritten note if possible)\n"
                "5. Update tracking spreadsheet\n\n"
                "### Monthly Partnership Routine (2 hrs/month)\n"
                "1. Reach out to 2-3 potential partners\n"
                "2. Follow up on existing partnership conversations\n"
                "3. Review partner referral numbers\n"
                "4. Send value to existing partners (share content, intro, etc.)"
            ),
            dynamic_prompt=(
                "Build the activation and tracking plan.\n\n"
                "Based on:\n"
                "- Time available: {Q45}\n"
                "- Tech comfort: {Q47}\n"
                "- Budget: {Q44}\n\n"
                "Produce:\n"
                "1. **Weekly referral routine** adapted to their time\n"
                "2. **Monthly partnership routine**\n"
                "3. **Tracking metrics**: referrals asked, referrals received, "
                "conversion rate, revenue from referrals\n"
                "4. **Simple tracking method** (spreadsheet template or CRM field)\n"
                "5. **3-month ramp-up plan**: Month 1 = referral system, "
                "Month 2 = first 3 partner outreaches, Month 3 = first co-marketing activity"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "All scripts must be complete and in English. "
                "Partnership proposal outline must be ready to customize and send."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q5", "Q7", "Q10", "Q11",
        "Q19", "Q22", "Q23", "Q24",
        "Q34", "Q44", "Q45", "Q47",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Focus on referrals from early clients. Too early for formal partnerships.",
        Maturity.GROWING: "Full referral + partnership system. This is the scaling lever.",
        Maturity.ESTABLISHED: "Formalize ambassador program. Commission structures for top referrers.",
        Maturity.PIVOT: "Leverage OLD network for referrals into new domain. Highest-value move.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Partnerships extend reach. Co-marketing is the priority.",
        Bottleneck.LEAD_GENERATION: "Referral system IS lead generation. Maximum depth.",
        Bottleneck.CONVERSION: "Referred leads convert 3-5x better. Amplify the referral channel.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Referral programs keep clients engaged (they become ambassadors).",
        Bottleneck.WRONG_CLIENTS: "Referrals from the RIGHT clients attract more right clients.",
    },
    quality_rules=[
        "Partner profiles must be specific — not 'other professionals' but named business types.",
        "Referral ask scripts must sound natural, not transactional.",
        "Incentive structures must be funded from the referred deal's margin, not existing margin.",
        "Partnership outreach must lead with THEIR benefit, not yours.",
        "Tracking method must match their tech level — a spreadsheet beats a CRM they won't use.",
        "Never recommend incentives that violate industry regulations (healthcare, legal, etc.).",
    ],
)