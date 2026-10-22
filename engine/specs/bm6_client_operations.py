"""BM6: Client Operations Playbook.

For ongoing or custom-scoped service delivery: onboarding, scope management,
contracts, communication, and scope creep prevention.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


BM6_SPEC = DocSpec(
    id=DocID.BM6,
    name="Client Operations Playbook",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Systematize the post-sale client experience: onboarding, scope definition, "
        "communication cadence, contract framework, and scope creep prevention. "
        "Turn chaotic engagements into repeatable, profitable processes."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Client Onboarding Flow",
            purpose="The first 48 hours after signing — set the tone for the entire engagement",
            tone_note="STARTER: build from scratch. ESTABLISHED: optimize what exists.",
            static_content=(
                "## The First 48 Hours Set the Relationship\n\n"
                "What happens right after the client signs determines:\n"
                "- Whether they feel confident or anxious about their purchase\n"
                "- Whether they become easy or difficult to work with\n"
                "- Whether they refer others or regret buying\n\n"
                "### The Onboarding Sequence\n"
                "| When | What | Who | Purpose |\n"
                "|------|------|-----|--------|\n"
                "| Immediately | Welcome email | Automated | Confirm, excite, set expectations |\n"
                "| Within 24h | Access & tools setup | You | Remove all technical barriers |\n"
                "| Day 1-2 | Kickoff call/meeting | You + client | Align on goals, timeline, communication |\n"
                "| Week 1 | Quick win delivery | You | Prove value FAST — Hormozi's 'speed to first value' |\n"
                "| Week 2 | First check-in | You | Address concerns before they fester |\n\n"
                "### Speed to First Value\n"
                "The fastest path to a delighted client: deliver a tangible result "
                "in the first 7 days. Not the FULL result — a meaningful partial one. "
                "An audit, a quick fix, a first draft, a setup complete."
            ),
            dynamic_prompt=(
                "Design the onboarding flow for this client's service.\n\n"
                "Based on:\n"
                "- Service delivered: {Q7}\n"
                "- Engagement type: {Q15}\n"
                "- Deal size: {Q10}\n"
                "- Business type: {Q1}\n\n"
                "Produce:\n"
                "1. **Welcome email** (full copy — subject + body)\n"
                "2. **Access/tools checklist** (what the client needs to provide/set up)\n"
                "3. **Kickoff meeting agenda** (5-7 bullet points, time allocation)\n"
                "4. **Quick win plan**: what they can deliver in the first 7 days "
                "   that's tangible and impressive\n"
                "5. **Client homework list**: what the client needs to do and by when\n\n"
                "If {Q15} = ongoing: onboarding leads into recurring cadence.\n"
                "If {Q15} = project-based: onboarding includes full scope confirmation."
            ),
        ),
        SectionSpec(
            name="Scope & Contract Framework",
            purpose="Protect profitability with clear scope definition and engagement terms",
            tone_note="Legal framing but accessible. Not a contract — a framework to adapt with a lawyer.",
            static_content=(
                "## Scope Definition Is Profit Protection\n\n"
                "Unclear scope is the #1 profitability killer for service businesses. "
                "'Can you also just quickly…' × 20 = half your margin gone.\n\n"
                "### The Scope Document Template\n"
                "Every engagement needs:\n"
                "1. **Objectives**: What success looks like (measurable)\n"
                "2. **Deliverables**: Exact list of what you'll produce\n"
                "3. **Exclusions**: What is NOT included (be explicit)\n"
                "4. **Timeline**: Milestones with dates\n"
                "5. **Assumptions**: What must be true for this to work\n"
                "6. **Change process**: How to handle scope changes (and what they cost)\n\n"
                "### Contract/Engagement Terms (General Framework)\n"
                "Key elements to include:\n"
                "- **Professional diligence clause**: commitment to best-effort delivery, "
                "not guaranteed specific outcomes (adapt to your jurisdiction's 'duty of care' standards)\n"
                "- **Payment terms** (from U4)\n"
                "- **Late payment penalties** (per applicable commercial law)\n"
                "- **IP ownership** (who owns the work product — usually client after full payment)\n"
                "- **Confidentiality** (NDA clause or reference)\n"
                "- **Termination**: notice period, pro-rata settlement, deliverable hand-off\n"
                "- **Liability cap**: standard is 1× engagement value\n\n"
                "⚠ This is a FRAMEWORK, not legal advice. Have a lawyer in your jurisdiction review your actual contract."
            ),
            dynamic_prompt=(
                "Build the scope and contract framework for this client.\n\n"
                "Based on:\n"
                "- Service: {Q7}\n"
                "- Engagement type: {Q15}\n"
                "- Deal size: {Q10}\n"
                "- Offer structure from U3/U4\n\n"
                "Produce:\n"
                "1. **Scope document template** with fill-in slots for each engagement:\n"
                "   [Client name], [Objectives], [Deliverables], [Exclusions], "
                "   [Timeline], [Assumptions], [Change process]\n"
                "2. **3 common 'scope creep' scenarios** for their business type "
                "   with suggested responses\n"
                "3. **Contract term suggestions** (adapt framework above to their service)\n"
                "4. **Termination clause** language appropriate for their engagement type\n\n"
                "If {Q15} = ongoing retainer: include review cadence and renewal terms.\n"
                "If {Q15} = project-based: include milestone-based payment triggers."
            ),
        ),
        SectionSpec(
            name="Communication Cadence",
            purpose="Set expectations for how and when you communicate with clients",
            tone_note="Boundaries. Without a cadence, clients text you at 11pm.",
            static_content=(
                "## Communication Rules\n\n"
                "### Cadence by Engagement Type\n"
                "| Type | Check-In | Report | Channel |\n"
                "|------|----------|--------|---------|\n"
                "| Retainer | Weekly | Monthly | Scheduled call + email |\n"
                "| Project (2-4 weeks) | 2× per week | Milestone | Email + Slack/Teams |\n"
                "| Project (2+ months) | Weekly | Bi-weekly | Scheduled call |\n\n"
                "### The Proactive Communication Rule\n"
                "If you update the client BEFORE they ask, you build trust.\n"
                "If they have to chase you for updates, you erode trust — even if the work is great.\n\n"
                "### Boundary Setting\n"
                "- State response time in your contract: 'within 24h on business days'\n"
                "- Urgent vs non-urgent: define what qualifies\n"
                "- Preferred channel: don't let clients scatter across email, WhatsApp, SMS, and DM"
            ),
            dynamic_prompt=(
                "Design the communication cadence for this client's engagements.\n\n"
                "Based on:\n"
                "- Engagement type: {Q15}\n"
                "- Ideal week: {Q43}\n"
                "- Team size: {Q4}\n"
                "- Time for marketing/sales: {Q45}\n\n"
                "Produce:\n"
                "1. **Check-in schedule** (frequency, format, duration)\n"
                "2. **Reporting template** (what to include in each update — 3-5 bullet structure)\n"
                "3. **Boundary rules**: response time, channels, availability hours\n"
                "4. **Escalation process**: what counts as urgent, how to handle it\n"
                "5. **Specific text for the 'communication rules' section** of their contract\n\n"
                "Match to their capacity. A solo consultant with 2-3 clients can do weekly calls. "
                "With 10 clients, it's email-first with monthly calls."
            ),
        ),
        SectionSpec(
            name="First-30-Days Quick Win Plan",
            purpose="Ensure the client sees value before buyer's remorse kicks in",
            tone_note="This is Hormozi's 'speed to first value' applied to service delivery.",
            static_content=(
                "## The 30-Day Value Sprint\n\n"
                "Buyer's remorse peaks in the first 2 weeks. "
                "If the client hasn't felt a tangible result by Day 14, "
                "they start questioning the purchase.\n\n"
                "### The Quick Win Framework\n"
                "1. **Day 1-3**: Low-effort, high-visibility win (an audit, a fix, a first draft)\n"
                "2. **Day 7-10**: Meaningful deliverable (something they can show their boss/partner)\n"
                "3. **Day 14**: Check-in with results data ('Here's what we've done, here's the impact')\n"
                "4. **Day 21-30**: First major milestone\n\n"
                "The quick win doesn't need to be the main deliverable. "
                "It needs to be VISIBLE and VALUABLE."
            ),
            dynamic_prompt=(
                "Design the 30-day quick win plan for this client's service.\n\n"
                "Based on:\n"
                "- Service: {Q7}\n"
                "- Typical deliverables\n"
                "- Client expectations\n\n"
                "Produce a day-by-day plan:\n"
                "| Day | Deliverable | Client Sees | Impact |\n\n"
                "The plan must show 3-4 tangible touchpoints where the client "
                "FEELS progress, not just knows work is happening.\n\n"
                "If {Q15} = project-based: map to the first major milestone.\n"
                "If {Q15} = retainer: map to the first monthly cycle."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Include the complete welcome email, "
                "kickoff agenda, scope template, and reporting template — all ready to use. "
                "Contract framework must reference applicable legal terms for the client's jurisdiction. Remember to use HTML only, not markdown."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q7", "Q8", "Q10",
        "Q15", "Q43", "Q45",
    ],
    upstream_deps=[DocID.U3, DocID.U4, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: (
            "Build the basics. They probably have no onboarding process. "
            "Start with the welcome email and a simple scope doc. Don't over-systematize."
        ),
        Maturity.GROWING: (
            "Formalize what's ad-hoc. They deliver well but it's chaotic. "
            "Full onboarding flow + scope template + communication cadence."
        ),
        Maturity.ESTABLISHED: (
            "Optimize for scale. They may be onboarding multiple clients simultaneously. "
            "Automate where possible. Train team members on the process."
        ),
        Maturity.PIVOT: (
            "New process for new service, but carry over operational maturity from old domain."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.RETENTION: (
            "THIS IS A PRIORITY. If clients buy but don't stay, the delivery experience is the issue. "
            "Full depth on onboarding, communication, and quick wins."
        ),
        Bottleneck.CONVERSION: "Post-sale experience reduces future objections (proof of great delivery).",
        Bottleneck.PRICING: "Strong operations justify higher prices — connect to U4.",
        Bottleneck.VISIBILITY: "Standard depth.",
        Bottleneck.LEAD_GENERATION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Scope definition must explicitly exclude out-of-scope requests.",
    },
    quality_rules=[
        "Welcome email must be complete — subject line, body, CTAs. Not a description of what to send.",
        "Scope template must include an EXCLUSIONS section. This is where scope creep is prevented.",
        "Contract framework must include professional diligence framing for service businesses.",
        "Communication cadence must respect the client's stated capacity (Q43, Q45).",
        "Quick win plan must identify something deliverable in the first 7 days — no exceptions.",
        "All templates must be usable immediately — fill in blanks and send.",
    ],
)