"""BM1: Sales Playbook.

The complete human sales process for businesses where a conversation
is required before the purchase happens.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


BM1_SPEC = DocSpec(
    id=DocID.BM1,
    name="Sales Playbook",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Build the complete consultative sales process from first contact to signed deal. "
        "Qualification criteria, call scripts, objection handling, proposal template, "
        "and follow-up protocol — one consolidated document for the entire human sales process."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Qualification Framework",
            purpose="Define who deserves a call and who doesn't — before wasting 30 minutes",
            tone_note="STARTER: may resist qualifying (afraid to turn anyone away). Explain why it's essential.",
            static_content=(
                "## Why Qualification Matters\n\n"
                "A 30-minute call costs you ~$50-150 in opportunity cost. "
                "If your close rate is 25%, 3 out of 4 calls are 'wasted.' "
                "Better qualification means fewer calls with higher close rates.\n\n"
                "### The BANT+ Framework\n"
                "| Criterion | Question | Must-Have? |\n"
                "|-----------|----------|------------|\n"
                "| **Budget** | Can they afford your solution? | Yes |\n"
                "| **Authority** | Can they say yes? | Yes |\n"
                "| **Need** | Do they have the problem you solve? | Yes |\n"
                "| **Timeline** | Do they need it now (not 'someday')? | Preferred |\n"
                "| **Fit** | Are they your ideal client profile? | Preferred |\n\n"
                "### Qualification Tiers\n"
                "- **A-lead**: meets all 5 → priority call, same day\n"
                "- **B-lead**: meets 3-4 → call within 48h\n"
                "- **C-lead**: meets 1-2 → nurture sequence (FC4), don't call yet\n"
                "- **Disqualified**: doesn't meet Budget or Need → polite redirect"
            ),
            dynamic_prompt=(
                "Build the qualification criteria for this client.\n\n"
                "Based on:\n"
                "- Ideal customer: {Q34}\n"
                "- Deal size: {Q10}\n"
                "- Decision maker: {Q17}\n"
                "- B2B target company: {Q38}, buyer role: {Q39}\n"
                "- Sales cycle: {Q16}\n\n"
                "Define:\n"
                "1. **5 qualification questions** to ask BEFORE the call "
                "(via form, email, or booking page)\n"
                "2. **Scoring**: how to rate A/B/C/Disqualified\n"
                "3. **Routing**: what happens to each tier "
                "(A → call, B → call with lower priority, C → lead magnet from FC2)\n"
                "4. **Disqualification script**: polite message for people who aren't a fit\n\n"
                "If {Q10} < $2000: lightweight qualification (2-3 questions). "
                "Don't make a $500 buyer fill a 10-field form."
            ),
        ),
        SectionSpec(
            name="Discovery & Closing Call Script",
            purpose="The actual conversation framework from hello to signed deal",
            tone_note="Natural, not robotic. A framework to internalize, not a teleprompter script.",
            static_content=(
                "## The Hormozi Call Structure\n\n"
                "### Phase 1: Rapport & Framing (2-3 min)\n"
                "- Thank them for their time\n"
                "- Set the agenda: 'I'll ask some questions to understand your situation, "
                "then if I think I can help, I'll explain how. If not, I'll tell you honestly.'\n"
                "- This framing removes sales pressure immediately.\n\n"
                "### Phase 2: Discovery (10-15 min)\n"
                "Use the SPIN sequence:\n"
                "- **Situation**: Where are you now? (facts)\n"
                "- **Problem**: What's not working? (pain)\n"
                "- **Implication**: What happens if you don't fix this? (consequences)\n"
                "- **Need-payoff**: What would it look like if this were solved? (dream outcome)\n\n"
                "Let THEM describe the pain. Don't diagnose too early.\n\n"
                "### Phase 3: Transition (1 min)\n"
                "'Based on what you've told me, I think I can help. Can I share how?'\n"
                "Wait for permission. This is critical.\n\n"
                "### Phase 4: Present the Offer (5-7 min)\n"
                "Present the value stack from U3, not a feature list.\n"
                "- 'Here's what we'd do for you…'\n"
                "- Walk through each component\n"
                "- State the price AFTER the full stack, not before\n\n"
                "### Phase 5: Handle Objections (5-10 min)\n"
                "See objection playbook below.\n\n"
                "### Phase 6: Close (2-3 min)\n"
                "- Assumptive close: 'Want to get started this week or next?'\n"
                "- Not 'So, what do you think?' (too passive)\n"
                "- If not ready: schedule a follow-up date, don't leave it open"
            ),
            dynamic_prompt=(
                "Adapt the call script for this client's specific situation.\n\n"
                "Inputs:\n"
                "- What they sell: {Q7}\n"
                "- Problem solved: {Q35}\n"
                "- Consequences of inaction: {Q36}\n"
                "- Alternatives: {Q37}\n"
                "- Proof: {Q32}, {Q33}\n"
                "- Offer structure from U3 (upstream)\n\n"
                "Produce:\n"
                "1. **5 SPIN discovery questions** customized to their domain\n"
                "   (not generic — reference their actual service)\n"
                "2. **Transition phrase** in their voice\n"
                "3. **Offer presentation outline** following U3 value stack order\n"
                "4. **3 closing phrases** they can actually say (natural, not cheesy)\n"
                "5. **Follow-up protocol**: what to send after the call "
                "(proposal timing, next steps email)\n\n"
                "Write in natural, conversational language that matches the client's "
                "business type and audience. Avoid corporate jargon."
            ),
        ),
        SectionSpec(
            name="Objection Playbook",
            purpose="Top 10 objections with specific rebuttals",
            tone_note="Empathetic, not adversarial. Objections are buying signals, not rejections.",
            static_content=(
                "## Objections Are Good\n\n"
                "If a prospect raises objections, they're interested enough to engage. "
                "No objections usually means no interest.\n\n"
                "### The 4-Step Rebuttal Framework\n"
                "1. **Acknowledge**: 'I completely understand…' (validate their concern)\n"
                "2. **Clarify**: 'When you say X, do you mean…?' (make sure you address the real issue)\n"
                "3. **Reframe**: Present the concern in a new light\n"
                "4. **Confirm**: 'Does that address your concern, or is there something else?'\n\n"
                "### The 5 Universal Objection Categories\n"
                "| Category | Real Meaning | Root Cause |\n"
                "|----------|-------------|------------|\n"
                "| **Price** | 'I don't see enough value' | Value stack wasn't compelling |\n"
                "| **Time** | 'I'm not sure this is urgent' | Implications weren't painful enough |\n"
                "| **Authority** | 'I can't decide alone' | Need to arm them for internal sale |\n"
                "| **Trust** | 'I'm not sure you can deliver' | Not enough proof |\n"
                "| **Need** | 'I'm not sure I need this' | Discovery was insufficient |"
            ),
            dynamic_prompt=(
                "Build the top 10 objections for THIS client's specific sales context.\n\n"
                "Based on:\n"
                "- Alternatives: {Q37} (what competitors/DIY options they'll mention)\n"
                "- Price point: {Q10}\n"
                "- Decision maker: {Q17}\n"
                "- Proof level: {Q32}\n"
                "- Business type: {Q1}\n\n"
                "For each objection:\n"
                "1. **The objection** (in the prospect's exact words)\n"
                "2. **What they really mean** (the underlying concern)\n"
                "3. **The rebuttal** (using the 4-step framework, written as dialogue)\n"
                "4. **Proof to deploy** (specific case study/result from {Q33} if available)\n\n"
                "Must include:\n"
                "- 'It's too expensive'\n"
                "- 'I need to think about it'\n"
                "- 'I found cheaper elsewhere'\n"
                "- 'I need to talk to [decision maker]'\n"
                "- At least 3 industry-specific objections\n\n"
                "Never use aggressive tactics. The tone is 'helpful advisor' not 'closer.'"
            ),
        ),
        SectionSpec(
            name="Proposal & Follow-Up Protocol",
            purpose="What happens after the call — proposal template and follow-up cadence",
            tone_note="Speed matters. Proposals sent within 2 hours close 3× more than those sent next week.",
            static_content=(
                "## Post-Call Protocol\n\n"
                "### Proposal Timing\n"
                "- **Same day** (within 2 hours of call): best close rate\n"
                "- **Next morning**: acceptable\n"
                "- **More than 48 hours**: you've lost momentum\n\n"
                "### Proposal Structure (1-2 pages max)\n"
                "1. **Situation summary**: 'You told me…' (prove you listened)\n"
                "2. **Recommended solution**: value stack from the call\n"
                "3. **Investment**: price + payment terms\n"
                "4. **Guarantee**: from U3\n"
                "5. **Next step**: ONE clear action ('Sign here' or 'Reply to confirm')\n\n"
                "### Follow-Up Cadence\n"
                "| Day | Action | Channel |\n"
                "|-----|--------|--------|\n"
                "| 0 | Send proposal | Email |\n"
                "| 2 | 'Did you have questions?' | Email |\n"
                "| 5 | Add value (relevant article/insight) | Email |\n"
                "| 8 | 'Still interested? Happy to jump on a quick call.' | Email or phone |\n"
                "| 14 | Final follow-up: 'I'll assume this isn't the right time.' | Email |\n\n"
                "After Day 14: move to long-term nurture (FC4). Don't keep chasing."
            ),
            dynamic_prompt=(
                "Build the proposal template and follow-up sequence for this client.\n\n"
                "Based on:\n"
                "- Offer: {Q7}\n"
                "- Deal size: {Q10}\n"
                "- Sales cycle: {Q16}\n"
                "- Offer structure from U3\n"
                "- Pricing from U4\n\n"
                "Produce:\n"
                "1. **Proposal template** with fill-in slots: "
                "[client name], [situation summary], [recommended package], [price], [guarantee], [next step]\n"
                "2. **5 follow-up email templates** (one per cadence step)\n"
                "3. **When to call instead of email** (deal size thresholds)\n\n"
                "If {Q10} < $2000: proposal = a clean email, not a PDF. "
                "Don't over-formalize a $500 deal.\n"
                "If {Q10} > $5000: structured PDF proposal with case studies."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "All scripts and rebuttals must be "
                "written as natural dialogue in <blockquote> blocks, not plain <ul> bullets. "
                "Include the proposal template with clear [SLOT] markers in <code> tags."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q10", "Q13", "Q16", "Q17",
        "Q32", "Q33", "Q34", "Q35", "Q36", "Q37",
        "Q38", "Q39",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U4, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: (
            "More hand-holding. They may never have done a sales call. "
            "Include 'what to do if you freeze' tips. Simpler script, fewer objection rebuttals."
        ),
        Maturity.GROWING: (
            "They've sold before but informally. Formalize what works, fix what doesn't. "
            "Full objection playbook."
        ),
        Maturity.ESTABLISHED: (
            "Optimization. They know their sales process — refine the weak spots. "
            "May need to train team members, so the playbook becomes a training document."
        ),
        Maturity.PIVOT: (
            "New domain, old skills. Adapt sales confidence from previous career. "
            "Biggest gap: new objections they haven't heard before."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.CONVERSION: (
            "THIS IS THE PRIORITY DOC. Maximum depth on all sections. "
            "If leads come in but don't convert, the sales process is broken. "
            "Extra attention to discovery (are they uncovering real pain?) and objections."
        ),
        Bottleneck.VISIBILITY: "Standard depth — the playbook exists but isn't the priority.",
        Bottleneck.PRICING: "Focus the pricing presentation section. The objection playbook emphasizes price rebuttals.",
        Bottleneck.LEAD_GENERATION: "Standard depth. If few leads exist, each call matters more — qualify carefully.",
        Bottleneck.RETENTION: "Light treatment on closing, heavier on the post-call experience.",
        Bottleneck.WRONG_CLIENTS: "Heavy emphasis on qualification. The playbook must REJECT bad-fit prospects.",
    },
    quality_rules=[
        "Scripts must sound like a real human, not a sales training manual.",
        "Objection rebuttals must be written as natural dialogue.",
        "The proposal template must be usable immediately — fill in blanks and send.",
        "Never recommend aggressive closing tactics. The tone is 'helpful expert advisor.'",
        "Follow-up sequence must have a defined END. Don't chase forever.",
        "If the client hates selling (Q49 signals), acknowledge it and frame the process as 'helping, not selling.'",
        "Qualification questions must be askable on a booking page or in a short email, not a 20-field form.",
    ],
)