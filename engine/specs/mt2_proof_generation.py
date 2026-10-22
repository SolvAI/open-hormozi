"""MT2: Proof Generation Plan.

For businesses with no or weak proof: strategy to build credibility
from zero to deployable in 30-60 days.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


MT2_SPEC = DocSpec(
    id=DocID.MT2,
    name="Proof Generation Plan",
    tier=Tier.MATURITY,
    purpose=(
        "Build proof from zero. Strategy to get first 2-3 case studies fast: "
        "beta/discounted offers, results documentation framework, testimonial capture protocol, "
        "and a 'proof sprint' timeline to go from zero to credible in 30-60 days."
    ),
    model_tier=ModelTier.HEAVY,
    sections=[
        SectionSpec(
            name="The Proof Sprint Strategy",
            purpose="Fast-track credibility from nothing",
            tone_note="STARTER/PIVOT: this is their #1 priority before spending on ads. Be direct about that.",
            static_content=(
                "## The Zero-to-Proof Playbook\n\n"
                "### The Problem\n"
                "No proof → can't charge full price → can't get great clients → can't generate proof.\n"
                "This is the credibility catch-22. Break it with a deliberate sprint.\n\n"
                "### The Sprint Framework\n"
                "```\n"
                "Week 1-2: Design the beta offer\n"
                "Week 3-4: Deliver to 2-3 beta clients\n"
                "Week 5-6: Document results + collect testimonials\n"
                "Week 7-8: Package into deployable assets\n"
                "```\n\n"
                "### Beta Offer Design Rules\n"
                "1. **Discounted, not free**: Free clients don't take it seriously. "
                "Charge 30-50% of target price.\n"
                "2. **Scope it tight**: 1 deliverable, 2-4 weeks, clear outcome\n"
                "3. **State the deal upfront**: 'Reduced price in exchange for a detailed case study, "
                "testimonial, and permission to use your results in my marketing.'\n"
                "4. **Target ideal-profile clients**: beta clients should be your ICP, not random\n"
                "5. **Over-deliver**: this IS your proof generation factory. Give 150%."
            ),
            dynamic_prompt=(
                "Design the proof sprint for this client.\n\n"
                "Based on:\n"
                "- Service: {Q7}\n"
                "- Target customer: {Q34}\n"
                "- Current proof: {Q32}\n"
                "- Deal size: {Q10}\n"
                "- Current network: {Q23}\n\n"
                "Produce:\n"
                "1. **Beta offer design**:\n"
                "   - What they deliver (scoped from {Q7})\n"
                "   - Beta price (30-50% of {Q10})\n"
                "   - Duration (2-4 weeks)\n"
                "   - What the beta client agrees to (testimonial, case study, results access)\n"
                "2. **Where to find 2-3 beta clients**:\n"
                "   - From existing network ({Q23})\n"
                "   - From LinkedIn/community outreach\n"
                "   - From referrals of friends/former colleagues\n"
                "3. **Beta pitch script** (email or DM — full copy)\n"
                "4. **Beta agreement outline** (what both sides commit to)\n\n"
                "If {Q32} = 'weak' (has experience but nothing documented): "
                "they may not need a beta — just retroactive documentation of past work."
            ),
        ),
        SectionSpec(
            name="Results Documentation Framework",
            purpose="Capture proof DURING delivery, not after",
            tone_note="If they wait until after to document, they'll forget the details. Build it into the process.",
            static_content=(
                "## The Documentation Habit\n\n"
                "### What to Capture (from Day 1)\n"
                "| Timing | What to Record | How |\n"
                "|--------|---------------|-----|\n"
                "| **Kickoff** | Client's starting state (numbers, situation, pain) | Notes + screenshot |\n"
                "| **Weekly** | Progress metrics, milestones hit, client feedback | Brief log |\n"
                "| **Delivery** | Final metrics, before/after comparison | Data export |\n"
                "| **Day 7 post** | Client's reaction, any early results | Email/call notes |\n"
                "| **Day 30 post** | Longer-term impact, ROI if measurable | Follow-up email |\n\n"
                "### The Results Log Template\n"
                "For each client engagement, maintain:\n"
                "```\n"
                "Client: [name]\n"
                "Start date: [date]\n"
                "Starting state: [specific metrics/situation]\n"
                "Goal: [what we aimed for]\n"
                "Week 1: [what we did + what changed]\n"
                "Week 2: [what we did + what changed]\n"
                "...\n"
                "End state: [specific metrics/situation]\n"
                "Delta: [before → after]\n"
                "Quote: [what the client said]\n"
                "```\n\n"
                "### Make It Effortless\n"
                "- Set a recurring 5-minute Friday reminder: 'Log this week's client progress'\n"
                "- Use a simple Google Doc or Notion page per client\n"
                "- Don't make it pretty — raw notes are fine. Polish when creating the case study."
            ),
            dynamic_prompt=(
                "Build the results documentation framework for this client's service.\n\n"
                "Based on:\n"
                "- Service: {Q7}\n"
                "- Engagement type: {Q15}\n"
                "- Typical deliverables\n\n"
                "Produce:\n"
                "1. **Results log template** customized for their service "
                "(what SPECIFIC metrics to track for their type of work)\n"
                "2. **Starting state questionnaire** (3-5 questions to ask at kickoff "
                "that establish the 'before' baseline)\n"
                "3. **End state questionnaire** (3-5 questions to ask at delivery "
                "that establish the 'after' state)\n"
                "4. **Weekly check-in template** (what to log each week)\n"
                "5. **Reminder system** recommendation (calendar event, tool, trigger)\n\n"
                "The metrics must be specific to their service type. "
                "A developer's results log ≠ a restaurant's ≠ a coach's."
            ),
        ),
        SectionSpec(
            name="Testimonial Capture Protocol",
            purpose="Get testimonials at the right moment with the right ask",
            tone_note="Timing is everything. Ask at peak satisfaction, with specific questions.",
            static_content=(
                "## The Testimonial Capture System\n\n"
                "### When to Ask (The Satisfaction Peak)\n"
                "Don't ask randomly. Ask when they're MOST delighted:\n"
                "- Right after a compliment ('That's so kind — would you mind putting that in writing?')\n"
                "- Right after a measurable result ('Your revenue is up 40%! Could I document this?')\n"
                "- Right after a milestone delivery\n"
                "- Right after they refer someone (they're already advocates)\n\n"
                "### The 3-Question Method\n"
                "Don't ask 'Can you write a testimonial?' (too hard, too vague).\n"
                "Ask 3 specific questions:\n"
                "1. 'What was your situation before we worked together?'\n"
                "2. 'What specific results have you seen?'\n"
                "3. 'What would you tell someone who's considering working with me?'\n\n"
                "Then YOU assemble their answers into a testimonial and ask for approval.\n\n"
                "### Formats to Capture\n"
                "| Format | Credibility | Effort |\n"
                "|--------|-----------|--------|\n"
                "| **Video** | Highest | High (need their time + camera) |\n"
                "| **Written + photo + name** | High | Medium |\n"
                "| **Google review** | High | Low |\n"
                "| **LinkedIn recommendation** | Medium-High | Low |\n"
                "| **Written, anonymous** | Low | Lowest |"
            ),
            dynamic_prompt=(
                "Build the testimonial capture system for this client.\n\n"
                "Produce:\n"
                "1. **Testimonial request email** (full copy — subject + body + the 3 questions)\n"
                "2. **In-person ask script** (for face-to-face services)\n"
                "3. **Video testimonial request** (including what to tell the client about format, "
                "length, and content)\n"
                "4. **Google review request** (with direct link instructions)\n"
                "5. **LinkedIn recommendation request** (with suggested talking points)\n"
                "6. **Follow-up if no response** (gentle nudge after 5 days)\n\n"
                "Each script in English. "
                "Match to their business type — a plumber's ask is different from a SaaS founder's."
            ),
        ),
        SectionSpec(
            name="30-60 Day Proof Sprint Timeline",
            purpose="Week-by-week plan from zero proof to deployable credibility",
            tone_note="Concrete timeline. Not 'build proof over time' but 'by Day 45, have 3 case studies.'",
            static_content=(
                "## The Proof Sprint Calendar\n\n"
                "| Week | Focus | Deliverable |\n"
                "|------|-------|------------|\n"
                "| **1** | Design beta offer + pitch 5 prospects | Beta offer document + 5 outreach messages |\n"
                "| **2** | Close 2-3 beta clients + start delivery | Signed agreements + kickoff logs |\n"
                "| **3-4** | Deliver beta + document everything | Weekly results logs |\n"
                "| **5** | Capture testimonials + measure results | 2-3 testimonials + before/after data |\n"
                "| **6** | Write case studies + create proof assets | Case study cards, logo wall draft |\n"
                "| **7** | Deploy proof on LP + proposals | Updated LP, proposal appendix |\n"
                "| **8** | Collect Google reviews + LinkedIn recs | 5+ reviews on public platforms |"
            ),
            dynamic_prompt=(
                "Build the proof sprint timeline for this client.\n\n"
                "Adapt the standard 8-week timeline to their situation:\n"
                "- Time available: {Q45}\n"
                "- Budget: {Q44}\n"
                "- Network: {Q23}\n"
                "- Current proof: {Q32}\n\n"
                "If {Q32} = 'weak' (has experience, nothing documented):\n"
                "  Sprint starts at Week 3 (skip beta, go straight to documenting past work).\n"
                "  List specific past clients to contact for retroactive testimonials.\n\n"
                "If {Q32} = 'none' (truly starting fresh):\n"
                "  Full 8-week sprint starting with beta offer.\n\n"
                "Produce the customized week-by-week plan with specific tasks and 'done' criteria."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Beta offer and all scripts must be "
                "complete and send-ready. Timeline must have specific weekly tasks."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q10", "Q15",
        "Q23", "Q32", "Q33",
        "Q44", "Q45",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.FC1, DocID.BM1],
    maturity_adaptations={
        Maturity.STARTER: "Full sprint. This is job #1 before any paid acquisition.",
        Maturity.GROWING: "Likely needs documentation of existing results, not beta offers.",
        Maturity.ESTABLISHED: "Should not be triggered — they have proof. If triggered, it's a gap to fill.",
        Maturity.PIVOT: (
            "Bridge proof: retroactive case studies from old domain reframed for new positioning. "
            "PLUS new beta offer for new domain."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Proof accelerates everything. Even ads convert better with proof.",
        Bottleneck.CONVERSION: "Proof IS the conversion tool. This is urgent.",
        Bottleneck.LEAD_GENERATION: "Lead magnets built from beta results are the most authentic.",
        Bottleneck.PRICING: "Proof justifies price. Sprint before raising prices.",
        Bottleneck.RETENTION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Beta clients must be IDEAL clients — proof attracts more of the same.",
    },
    quality_rules=[
        "Beta offer must be genuinely valuable — not a watered-down version of the real service.",
        "Beta price must be 30-50% of target, never free.",
        "Results log template must have metrics specific to their service type.",
        "Testimonial requests must use the 3-question method, not 'please write a review.'",
        "Timeline must be realistic for their available time.",
        "If they have past clients they can contact, retroactive documentation comes before beta.",
    ],
)