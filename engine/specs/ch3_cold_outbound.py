# CH3 - Cold Outbound Playbook spec
"""CH3: Cold Outbound Playbook.

B2B cold email and LinkedIn outreach: targeting, sequences,
personalization, tools, and RGPD compliance.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


CH3_SPEC = DocSpec(
    id=DocID.CH3,
    name="Cold Outbound Playbook",
    tier=Tier.CHANNEL,
    purpose=(
        "Build the complete cold outreach system: targeting criteria, list building, "
        "email sequences, LinkedIn sequences, personalization frameworks, "
        "reply handling, and RGPD-compliant execution."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Targeting & List Building",
            purpose="Define exactly who to reach out to and how to find them",
            tone_note="Precision > volume. 50 perfect prospects beat 500 random ones.",
            static_content=(
                "## The Targeting Hierarchy\n\n"
                "1. **Company profile**: industry, size, revenue, location, tech stack\n"
                "2. **Buyer persona**: role, seniority, decision authority\n"
                "3. **Timing signal**: hiring, funding, growth, new exec, problem indicator\n\n"
                "### List Building Tools\n"
                "| Tool | Best For | Cost | Data Quality |\n"
                "|------|----------|------|-------------|\n"
                "| **LinkedIn Sales Navigator** | B2B company + person search | ~$80/mo | High |\n"
                "| **Apollo.io** | Email finding + sequences | Free-$50/mo | Medium-High |\n"
                "| **ZoomInfo** | Enterprise B2B data | $150+/mo | High |\n"
                "| **Hunter.io** | Email verification | Free-$50/mo | Medium |\n"
                "| **Lusha** | Contact enrichment | Free-$50/mo | Medium-High |\n\n"
                "### List Quality Rules\n"
                "- Verify every email before sending (bounce rate must stay <3%)\n"
                "- Enrich with at least 1 personalization data point per prospect\n"
                "- Max list size per sequence: 50-100 (you need to personalize)\n"
                "- Refresh lists monthly (people change roles)"
            ),
            dynamic_prompt=(
                "Build the targeting criteria for this client.\n\n"
                "Based on:\n"
                "- ICP from U2: {Q34}\n"
                "- B2B target: {Q38} (company size), {Q39} (buyer role)\n"
                "- Industry: {Q2}\n"
                "- Geography: {Q5}\n"
                "- Problem solved: {Q35}\n\n"
                "Produce:\n"
                "1. **Company filter** (industry, size, revenue range, location)\n"
                "2. **Person filter** (title, seniority, department)\n"
                "3. **Timing signals** (what events make them more receptive NOW)\n"
                "4. **Recommended tools** for this specific market\n"
                "5. **List building walkthrough**: step-by-step in LinkedIn Sales Nav or Apollo\n"
                "6. **Initial list size target** and weekly prospecting volume"
            ),
        ),
        SectionSpec(
            name="Cold Email Sequence",
            purpose="The 3-5 email sequence that gets replies",
            tone_note="Short. Personal. No 'I hope this email finds you well.' Every word earns its place.",
            static_content=(
                "## Cold Email Principles\n\n"
                "### The Only Metric That Matters: Reply Rate\n"
                "- Good: 5-10% reply rate\n"
                "- Great: 10-20%\n"
                "- Below 3%: something is broken (targeting, subject, or copy)\n\n"
                "### The 3-Line Email Framework\n"
                "1. **Line 1: Personalized opener** (prove you researched them)\n"
                "2. **Line 2: Value proposition** (what you can do for THEM, not about you)\n"
                "3. **Line 3: Soft CTA** (question, not a demand)\n\n"
                "### What NOT to Do\n"
                "- Long emails (>150 words = ignored)\n"
                "- Attachments in first email (spam filter)\n"
                "- Multiple CTAs ('book a call OR visit our site OR reply')\n"
                "- Fake personalization ('I saw your LinkedIn and was impressed')\n"
                "- HTML-heavy design (use plain text)\n\n"
                "### Sequence Cadence\n"
                "| Email | When | Purpose |\n"
                "|-------|------|--------|\n"
                "| 1 | Day 0 | Initial outreach |\n"
                "| 2 | Day 3 | Follow-up (add value) |\n"
                "| 3 | Day 7 | Different angle |\n"
                "| 4 | Day 14 | Social proof or case study |\n"
                "| 5 | Day 21 | Break-up email ('Should I close your file?') |"
            ),
            dynamic_prompt=(
                "Write the complete 5-email cold sequence for this client.\n\n"
                "Based on:\n"
                "- What they sell: {Q7}\n"
                "- Problem solved: {Q35}\n"
                "- Proof: {Q33}\n"
                "- Target buyer: {Q34}, {Q39}\n"
                "- Messaging angles from U5\n\n"
                "For each email:\n"
                "1. **Subject line** (A/B version: 2 options)\n"
                "2. **Full body** (max 100 words for emails 1-3, up to 150 for email 4)\n"
                "3. **Personalization slots**: [COMPANY], [FIRST_NAME], [TRIGGER], [CUSTOM]\n"
                "4. **CTA**: the one thing you want them to do\n\n"
                "Email 1: personalized opener + value prop + soft question.\n"
                "Email 2: follow-up, add one insight or different angle.\n"
                "Email 3: social proof or case study snippet.\n"
                "Email 4: different approach entirely (new angle from U5).\n"
                "Email 5: break-up ('Should I close your file?').\n\n"
                "Write in English."
            ),
        ),
        SectionSpec(
            name="LinkedIn DM Sequence",
            purpose="Parallel LinkedIn touchpoints that complement email",
            tone_note="LinkedIn is warmer than email. The approach should feel like networking, not spam.",
            static_content=(
                "## LinkedIn Outreach Rules\n\n"
                "### Connection Request\n"
                "- Max 300 chars. Must feel personal.\n"
                "- Reference something specific (their post, company news, mutual connection)\n"
                "- Do NOT pitch in the connection request\n\n"
                "### Message Sequence (post-connection)\n"
                "| Message | When | Approach |\n"
                "|---------|------|----------|\n"
                "| 1 | Day 1 after accept | Thank + open-ended question about their work |\n"
                "| 2 | Day 3-5 | Share relevant insight/content (give value first) |\n"
                "| 3 | Day 7-10 | Bridge to your offer (only if engaged) |\n\n"
                "### LinkedIn + Email Multichannel\n"
                "Day 0: Email 1\n"
                "Day 1: LinkedIn connection request\n"
                "Day 3: Email 2\n"
                "Day 5: LinkedIn message 1 (if connected)\n"
                "Day 7: Email 3\n"
                "…etc. Alternate channels. Never hit both on the same day."
            ),
            dynamic_prompt=(
                "Write the LinkedIn sequence for this client.\n\n"
                "Based on:\n"
                "- Target buyer role: {Q39}\n"
                "- Their LinkedIn presence: {Q31}\n"
                "- Service: {Q7}\n"
                "- Problem: {Q35}\n\n"
                "Produce:\n"
                "1. **Connection request** (2 versions, max 300 chars each)\n"
                "2. **Follow-up message 1** (thank you + question)\n"
                "3. **Value message 2** (share insight relevant to their role)\n"
                "4. **Bridge message 3** (transition to offer)\n"
                "5. **Multichannel calendar**: email + LinkedIn timing for a 21-day sequence"
            ),
        ),
        SectionSpec(
            name="Reply Handling & Privacy Compliance",
            purpose="What to do when they reply (positive, negative, or neutral) + legal compliance",
            tone_note="Legal compliance is non-negotiable. Privacy violations = real fines.",
            static_content=(
                "## Reply Types & Responses\n\n"
                "| Reply Type | Response Framework |\n"
                "|-----------|-------------------|\n"
                "| **Interested** | Propose a specific time (don't ask 'when works for you?') |\n"
                "| **Not now** | Thank + ask permission to follow up in X months |\n"
                "| **Not interested** | Thank + remove from sequence. No arguing. |\n"
                "| **Hostile** | Apologize briefly + immediately unsubscribe. |\n"
                "| **Referral** | Thank profusely + ask for intro (not just the name) |\n\n"
                "## Privacy Compliance for Cold Outreach\n\n"
                "### B2B Cold Email (General Framework)\n"
                "- **Legal basis varies by jurisdiction**: legitimate interest (GDPR/EU), "
                "CAN-SPAM (US), CASL (Canada), etc.\n"
                "- **Universal requirements**:\n"
                "  - Identify yourself clearly (name, company)\n"
                "  - State why you're contacting them\n"
                "  - Include an easy opt-out in every email\n"
                "  - Honor opt-outs within 48h (10 business days max under CAN-SPAM)\n"
                "  - Keep a suppression list\n"
                "- **B2C cold email**: generally requires prior consent in most jurisdictions. "
                "Verify local rules before sending.\n"
                "- **LinkedIn DMs**: platform ToS apply in addition to privacy law\n\n"
                "⚠ This is guidance, not legal advice. Consult a privacy/compliance specialist "
                "for your specific jurisdiction."
            ),
            dynamic_prompt=(
                "Build the reply handling scripts and compliance setup.\n\n"
                "Produce:\n"
                "1. **Reply templates** for each scenario (interested / not now / not interested / referral)\n"
                "2. **Privacy compliance checklist** specific to their outreach:\n"
                "   - Email footer text\n"
                "   - Opt-out mechanism\n"
                "   - Data retention policy\n"
                "   - Suppression list management\n"
                "3. **Daily execution routine**: how many prospects, what order, what tools\n"
                "4. **Volume recommendation**: daily sends based on their available time ({Q45})"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "All emails must be complete — "
                "full subject lines, full body text, personalization slots marked as [VARIABLE]. "
                "LinkedIn messages must respect character limits.\n\n"
                "In the tools section, include this resource for prospect tracking:\n"
                "'For a free CRM/prospect tracker, see Notion's CRM templates: "
                "https://www.notion.com/templates/category/best-crm-templates'"
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q5", "Q7", "Q10",
        "Q31", "Q33", "Q34", "Q35",
        "Q38", "Q39", "Q44", "Q45",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U7, DocID.U8, DocID.FC1],
    maturity_adaptations={
        Maturity.STARTER: "Low volume (10-20/week). Focus on personalization quality over quantity.",
        Maturity.GROWING: "Scale to 30-50/week. Add LinkedIn multichannel.",
        Maturity.ESTABLISHED: "Systematic: CRM integration, templates library, team delegation.",
        Maturity.PIVOT: "Leverage old network for warm intros alongside cold outreach.",
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Outbound IS the visibility channel. Maximum depth on sequences.",
        Bottleneck.LEAD_GENERATION: "Focus on reply rate optimization and list quality.",
        Bottleneck.CONVERSION: "Outbound generates qualified conversations. Script quality is key.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Not applicable for retention. Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Targeting precision is everything. Better list = better clients.",
    },
    quality_rules=[
        "Cold emails must be under 150 words. Count them.",
        "LinkedIn connection requests must be under 300 characters.",
        "Privacy compliance section is mandatory — never skip it.",
        "Personalization must be REAL: reference specific company/role data, not fake flattery.",
        "Break-up email must be included. The sequence has a defined end.",
        "Volume recommendations must respect stated available time (Q45).",
        "Tools recommended must match budget — don't prescribe $200/mo tools to a $0 budget.",
    ],
)