"""CH7: Marketplace Strategy.

For clients dependent on a marketplace: optimize there while
building a migration path to an owned channel.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH7_SPEC = DocSpec(
    id=DocID.CH7,
    name="Marketplace Strategy",
    tier=Tier.CHANNEL,
    purpose=(
        "Optimize performance on the current marketplace while building a systematic "
        "migration plan to an owned channel. Always transitional — never the long-term answer."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Marketplace Profile Optimization",
            purpose="Maximize conversion and visibility on the current platform",
            tone_note="Pragmatic. They're on the marketplace NOW — help them succeed there while they migrate.",
            static_content=(
                "## Marketplace Ranking Factors\n\n"
                "Most marketplaces rank profiles by:\n"
                "1. **Reviews & ratings**: quantity + recency + score\n"
                "2. **Response time**: faster = higher ranking\n"
                "3. **Completion rate**: do you deliver what you promise?\n"
                "4. **Profile completeness**: photo, bio, portfolio, skills, pricing\n"
                "5. **Activity**: regular logins, proposals, messages\n\n"
                "### Profile Optimization Checklist\n"
                "- [ ] Professional headshot (not a logo for personal services)\n"
                "- [ ] Headline: outcome-focused, not role-focused\n"
                "  - ❌ 'Full-Stack React/Node Developer'\n"
                "  - ✅ 'I turn your idea into a working product in 6 weeks'\n"
                "- [ ] Description: SPIN structure (Situation → Problem → Implication → Solution)\n"
                "- [ ] Portfolio: 3-5 best projects with visible results\n"
                "- [ ] Pricing: positioned in the top 30% (not cheapest)\n"
                "- [ ] Skills/tags: all relevant ones selected\n"
                "- [ ] Availability: updated and accurate"
            ),
            dynamic_prompt=(
                "Optimize the marketplace profile for this client.\n\n"
                "Based on:\n"
                "- Which marketplace: derive from {Q23}, {Q26}\n"
                "- Service: {Q7}\n"
                "- Proof: {Q32}, {Q33}\n"
                "- Pricing: {Q9}, {Q10}\n"
                "- Positioning from U5\n\n"
                "Produce:\n"
                "1. **Optimized headline** (apply U5 positioning to marketplace format)\n"
                "2. **Optimized description** (full text, marketplace-length)\n"
                "3. **Portfolio strategy**: which projects to showcase, how to present results\n"
                "4. **Pricing strategy**: where to position on the marketplace price spectrum\n"
                "5. **Review acceleration**: how to get 5-10 reviews fast "
                "(over-deliver on first projects, timing of the ask)\n"
                "6. **Response time optimization**: target response time, notification setup"
            ),
        ),
        SectionSpec(
            name="Client-to-Direct Conversion",
            purpose="Turn marketplace clients into direct clients (the core migration move)",
            tone_note="This must respect marketplace ToS. Some prohibit direct contact solicitation.",
            static_content=(
                "## The Migration Playbook\n\n"
                "### The Legitimate Path\n"
                "Most marketplaces allow direct work with clients you've ALREADY worked with on the platform. "
                "The path:\n"
                "1. **Deliver exceptional work** on the marketplace (earn the relationship)\n"
                "2. **Over-deliver**: give more than expected (creates reciprocity)\n"
                "3. **Build the relationship**: become their trusted advisor, not a vendor\n"
                "4. **For the NEXT project**: propose working directly\n"
                "   - 'For this next phase, I can offer you [better terms/more flexibility/faster delivery] "
                "   if we work directly. Here's my direct proposal.'\n\n"
                "### What NOT to Do\n"
                "- Don't solicit direct work in the FIRST engagement (violates most ToS)\n"
                "- Don't badmouth the marketplace to the client\n"
                "- Don't include your contact info in marketplace messages (often monitored)\n"
                "- Don't undercut your marketplace price (races to the bottom)\n\n"
                "### The 'Owned Channel' Mention\n"
                "In your marketplace profile and after-project follow-up:\n"
                "'For direct projects and exclusive offers, visit: [website]'\n"
                "This is generally acceptable — you're promoting your brand, not soliciting."
            ),
            dynamic_prompt=(
                "Build the marketplace-to-direct conversion plan.\n\n"
                "Based on:\n"
                "- Marketplace dependency: {Q26}\n"
                "- Current deal size: {Q10}\n"
                "- Repeat potential: {Q11}\n"
                "- Website: {Q28}\n\n"
                "Produce:\n"
                "1. **Conversion talking points**: what to say to marketplace clients about working direct\n"
                "2. **Value proposition for going direct**: why it's better FOR THEM (not just you)\n"
                "3. **Transition offer**: a special deal for marketplace clients who switch\n"
                "4. **Legal safeguards**: what the specific marketplace's ToS allows/prohibits\n"
                "5. **Post-project follow-up sequence** that naturally leads to direct relationship\n\n"
                "If {Q26} = 'only source': migration is critical but must be gradual. "
                "Don't burn the marketplace bridge before the owned channel works."
            ),
        ),
        SectionSpec(
            name="Migration Timeline & Dependency Reduction",
            purpose="Structured plan to reduce marketplace dependency over 3-6 months",
            tone_note="Realistic. Going from 100% marketplace to 0% takes 6-12 months, not 4 weeks.",
            static_content=(
                "## The Dependency Reduction Plan\n\n"
                "### Target Milestones\n"
                "| Month | Marketplace % | Direct % | Focus |\n"
                "|-------|-------------|---------|-------|\n"
                "| Current | 80-100% | 0-20% | Optimize marketplace profile |\n"
                "| Month 2 | 70% | 30% | Launch owned channel, convert 1 client |\n"
                "| Month 4 | 50% | 50% | Owned channel producing leads |\n"
                "| Month 6 | 30% | 70% | Marketplace is supplementary |\n"
                "| Month 9-12 | 10-20% | 80-90% | Marketplace for overflow only |\n\n"
                "### The Exit Strategy is NOT Quitting the Marketplace\n"
                "Keep the marketplace profile active even at 10%. It provides:\n"
                "- Social proof (reviews visible to potential direct clients)\n"
                "- Overflow capacity (when your pipeline is full)\n"
                "- Market intelligence (what clients are asking for)"
            ),
            dynamic_prompt=(
                "Build the migration timeline for this client.\n\n"
                "Based on:\n"
                "- Current dependency: {Q26}\n"
                "- Recommended primary channel: {channel}\n"
                "- Budget for owned channel: {Q44}\n"
                "- Time available: {Q45}\n\n"
                "Produce:\n"
                "1. **6-month migration timeline** with monthly targets\n"
                "2. **Parallel execution plan**: what to do on marketplace + owned channel simultaneously\n"
                "3. **Revenue risk management**: how to maintain income during transition\n"
                "4. **Decision points**: when to reduce marketplace effort, when to increase owned channel\n"
                "5. **Success criteria**: how to know the migration is working\n\n"
                "If {Q26} = '100% dependent': add a 'Month 0' that's purely marketplace optimization. "
                "Don't start migration until owned channel is functional."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Marketplace profile optimization must "
                "include the complete rewritten headline and description. "
                "Migration timeline must have specific monthly targets."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q9", "Q10", "Q11",
        "Q23", "Q26", "Q28",
        "Q32", "Q33", "Q44", "Q45",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U9],
    maturity_adaptations={
        Maturity.STARTER: "Marketplace is the right starting point. Optimize there WHILE building owned channel.",
        Maturity.GROWING: "Migration is the priority. You've validated demand — now own the channel.",
        Maturity.ESTABLISHED: "Should already be mostly direct. Marketplace is for overflow only.",
        Maturity.PIVOT: "New marketplace for new domain may be useful as proof-building springboard.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Marketplace provides visibility — use it. But migrate to owned visibility.",
        Bottleneck.LEAD_GENERATION: "The marketplace IS generating leads. Build an owned lead engine in parallel.",
        Bottleneck.CONVERSION: "Marketplace handles conversion. Learn what converts there, apply to owned channel.",
        Bottleneck.PRICING: "Marketplace creates price pressure. Migration enables premium pricing.",
        Bottleneck.RETENTION: "Convert marketplace clients to direct for retention. Marketplace makes loyalty hard.",
        Bottleneck.WRONG_CLIENTS: "Marketplace attracts price-shoppers. Migration filters for quality.",
    },
    quality_rules=[
        "Always respect marketplace ToS in recommendations. Don't advise ToS violations.",
        "Migration timeline must be gradual — don't recommend quitting the marketplace cold turkey.",
        "Profile optimization must include complete rewritten text, not just tips.",
        "Conversion scripts must provide value to the CLIENT, not just benefit the freelancer.",
        "Revenue risk during migration must be explicitly addressed.",
        "CH7 is ALWAYS paired with a second channel recommendation for migration.",
    ],
)