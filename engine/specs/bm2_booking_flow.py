"""BM2: Booking & Scheduling Flow.

For appointment-based businesses: the complete scheduling system
from booking to confirmation to no-show recovery.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


BM2_SPEC = DocSpec(
    id=DocID.BM2,
    name="Booking & Scheduling Flow",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Design the complete booking experience: scheduling tool setup, availability logic, "
        "reminder sequences, no-show prevention, booking page copy, "
        "and pre-appointment preparation."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Scheduling Tool & Availability",
            purpose="Choose the right tool and configure availability windows",
            tone_note="Practical. Match tool complexity to tech level. Calendly isn't the only option.",
            static_content=(
                "## Scheduling Tool Options\n\n"
                "| Tool | Best For | Cost | Complexity |\n"
                "|------|----------|------|------------|\n"
                "| **Calendly** | Solo consultants, coaches | Free-$12/mo | Low |\n"
                "| **Cal.com** | Open-source alternative | Free-$15/mo | Low-Medium |\n"
                "| **Acuity (Squarespace)** | Service businesses, intake forms | $16-46/mo | Medium |\n"
                "| **SimplyBook.me** | Multi-service (salons, practices) | Free-$50/mo | Medium |\n"
                "| **Google Calendar** | Minimal setup, manual flow | Free | Lowest |\n\n"
                "### Availability Design Rules\n"
                "1. **Don't show all available time.** Fewer slots = more perceived demand.\n"
                "2. **Buffer time**: 15-30 min between appointments (travel, prep, breathing room)\n"
                "3. **Minimum notice**: 24h for free consultations, 2h for paid services\n"
                "4. **Maximum advance booking**: 2-4 weeks. Beyond that, no-show rate skyrockets.\n"
                "5. **Batch similar appointments**: all discovery calls on Tue/Thu afternoons, "
                "not scattered across every day."
            ),
            dynamic_prompt=(
                "Recommend the scheduling setup for this client.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Service delivered: {Q7}\n"
                "- Tech comfort: {Q47}\n"
                "- Team size: {Q4}\n"
                "- Budget: {Q44}\n\n"
                "Specify:\n"
                "1. **Recommended tool** with rationale\n"
                "2. **Availability windows** (which days, which hours, buffer time)\n"
                "3. **Appointment types** if multiple exist "
                "(e.g., '15-min discovery call' vs '60-min consultation')\n"
                "4. **Batch schedule** recommendation for their ideal week ({Q43})\n\n"
                "If {Q1} = consultant/coach: focus on discovery call scheduling.\n"
                "If {Q1} = practitioner/dentist: focus on multi-service booking.\n"
                "If {Q1} = tradesperson: focus on quote visit scheduling."
            ),
        ),
        SectionSpec(
            name="Booking Page Copy",
            purpose="What the prospect sees and reads when they're about to book",
            tone_note="Conversion-focused. The booking page is a mini landing page.",
            static_content=(
                "## The Booking Page Is a Sales Page\n\n"
                "Most booking pages are just a calendar widget. Missed opportunity.\n\n"
                "### What a Booking Page Needs\n"
                "1. **Headline**: What they'll get from this appointment (outcome, not activity)\n"
                "   - ❌ 'Book a call with Thomas'\n"
                "   - ✅ 'Book your free 20-min strategy session — we'll map your growth plan'\n"
                "2. **What to expect**: 2-3 bullets on what happens during the appointment\n"
                "3. **Who it's for**: 1 sentence qualifier ('For CTOs of startups with...')\n"
                "4. **Social proof**: 1 testimonial or result\n"
                "5. **Calendar widget**: the actual scheduling tool\n"
                "6. **FAQ**: 'Is it free?', 'How long?', 'What do I need to prepare?'"
            ),
            dynamic_prompt=(
                "Write the complete booking page copy for this client.\n\n"
                "Based on:\n"
                "- Service: {Q7}\n"
                "- Target audience: {Q34}\n"
                "- Problem solved: {Q35}\n"
                "- Proof: {Q32}, {Q33}\n"
                "- Positioning from U5\n\n"
                "Produce:\n"
                "1. **Headline** (outcome-driven)\n"
                "2. **What to expect** (3 bullets)\n"
                "3. **Who it's for** (1 sentence)\n"
                "4. **Social proof** (from {Q33} or a placeholder format)\n"
                "5. **FAQ** (3-4 questions and answers)\n"
                "6. **CTA button text** (not 'Submit' — something compelling)\n\n"
                "The tone should match U5 guidelines."
            ),
        ),
        SectionSpec(
            name="Reminder & Confirmation Sequence",
            purpose="Reduce no-shows from 20-30% to under 10%",
            tone_note="Automated. This runs without human intervention once set up.",
            static_content=(
                "## The No-Show Problem\n\n"
                "Industry average no-show rate: 20-30% for free consultations, 5-10% for paid.\n"
                "Every no-show costs you the slot + the opportunity cost of someone who would have shown up.\n\n"
                "### The 3-Touch Reminder Sequence\n"
                "| When | Channel | Content |\n"
                "|------|---------|--------|\n"
                "| **Immediately** | Email | Confirmation + calendar invite + prep instructions |\n"
                "| **24 hours before** | Email + SMS | Reminder + 'reply to confirm or reschedule' |\n"
                "| **1 hour before** | SMS | Quick reminder + link/address |\n\n"
                "### No-Show Policy\n"
                "- **Free consultations**: 1 reschedule allowed, then disqualified\n"
                "- **Paid services**: charge 50% no-show fee (state in booking confirmation)\n"
                "- **Recovery**: send a 'we missed you' message within 1 hour with reschedule link"
            ),
            dynamic_prompt=(
                "Write the complete reminder sequence for this client.\n\n"
                "Based on:\n"
                "- Appointment type: {Q7}\n"
                "- Free or paid appointment: derive from {Q13}, {Q10}\n"
                "- Business type: {Q1}\n\n"
                "Produce:\n"
                "1. **Confirmation email** (full copy — subject line + body)\n"
                "2. **24h reminder** (email + optional SMS text)\n"
                "3. **1h reminder** (SMS text)\n"
                "4. **No-show recovery message** (sent 30 min after no-show)\n"
                "5. **No-show policy text** for the booking page\n\n"
                "If free discovery call: the confirmation should reinforce value "
                "('Here's what we'll cover') to reduce no-shows.\n"
                "If paid service: include cancellation/reschedule policy compliant "
                "with applicable consumer protection law in the client's jurisdiction."
            ),
        ),
        SectionSpec(
            name="Pre-Appointment Questionnaire",
            purpose="Gather intel before the meeting to make the appointment more productive",
            tone_note="Only for consultative/service appointments. Skip for simple bookings.",
            static_content=(
                "## Why Pre-Qualify Before the Call\n\n"
                "A 5-question pre-appointment form:\n"
                "- Saves 5-10 minutes of basic discovery ON the call\n"
                "- Lets you prepare (research their company, customize your pitch)\n"
                "- Acts as a soft commitment device (invested time = more likely to show)\n"
                "- Disqualifies mismatches before wasting anyone's time\n\n"
                "### Rules\n"
                "- **Max 5 questions** (more = drop-off)\n"
                "- **1 open-ended, 4 structured** (dropdown/radio)\n"
                "- Send it IN the confirmation email, not as a separate step"
            ),
            dynamic_prompt=(
                "Design the pre-appointment questionnaire for this client.\n\n"
                "Based on:\n"
                "- Service: {Q7}\n"
                "- Qualification criteria from the Qualification Framework section above\n"
                "- Decision maker: {Q17}\n"
                "- B2B target: {Q38}, {Q39}\n\n"
                "Produce:\n"
                "1. **5 questions** (type: text, dropdown, or radio for each)\n"
                "2. **Why each question matters** (what you'll do with the answer)\n"
                "3. **Red flag answers** (responses that signal disqualification)\n\n"
                "If {Q10} < $1000: skip the questionnaire. It's overkill for small deals. "
                "State this explicitly."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "All email/SMS copy must be "
                "complete and ready to use — full subject lines, full body text. "
                "Booking page copy in a clearly marked <h3> section. Use <table> for scheduling grids."
            ),
        ),
        FormatSpec(
            format=Format.MERMAID,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate a Mermaid flowchart TD showing the complete booking flow.\n"
                "Nodes: Booking Page → Confirmation → 24h Reminder → 1h Reminder → "
                "Appointment → (Showed / No-Show).\n"
                "Include the no-show recovery branch.\n"
                "Quote all labels. Max 12 nodes."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q7", "Q10", "Q13", "Q14", "Q17",
        "Q32", "Q33", "Q34", "Q35",
        "Q38", "Q39", "Q43", "Q44", "Q47",
    ],
    upstream_deps=[DocID.U2, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: "Simplest possible setup. Calendly free tier + manual confirmation email.",
        Maturity.GROWING: "Full flow. Automated reminders. Pre-appointment questionnaire.",
        Maturity.ESTABLISHED: "Multi-service booking, team scheduling, intake forms, CRM integration.",
        Maturity.PIVOT: "New booking flow for new service. Leverage old scheduling habits.",
    },
    bottleneck_adaptations={
        Bottleneck.CONVERSION: "Booking page copy is critical — it's the last step before commitment.",
        Bottleneck.VISIBILITY: "Standard depth.",
        Bottleneck.LEAD_GENERATION: "Booking page IS the lead capture. Extra copy attention.",
        Bottleneck.PRICING: "Standard depth.",
        Bottleneck.RETENTION: "Add rebooking CTA to post-appointment follow-up.",
        Bottleneck.WRONG_CLIENTS: "Pre-appointment questionnaire must filter aggressively.",
    },
    quality_rules=[
        "All email/SMS copy must be complete — no '[insert your text here]' placeholders.",
        "Reminder timing must account for the business type — a dentist reminder ≠ a coach reminder.",
        "No-show policy must be fair and legally compliant (consumer law for paid services).",
        "Pre-appointment questionnaire: max 5 questions. Period. No exceptions.",
        "Tool recommendation must match their budget and tech level — don't prescribe Acuity to someone who struggles with email.",
    ],
)