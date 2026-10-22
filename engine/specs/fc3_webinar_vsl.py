"""FC3: Webinar / VSL Script.

Full presentation script for education-then-sell: webinar, VSL,
workshop, or masterclass format.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


FC3_SPEC = DocSpec(
    id=DocID.FC3,
    name="Webinar / VSL Script",
    tier=Tier.FUNNEL,
    purpose=(
        "Write the complete script for a webinar, VSL, or workshop that educates "
        "the audience and naturally transitions into the offer. Includes registration "
        "page copy, reminder sequence, slide outline, and replay strategy."
    ),
    model_tier=ModelTier.HEAVY,
    sections=[
        SectionSpec(
            name="Registration Page & Promotion",
            purpose="Get people to sign up and show up",
            tone_note="Registration page = mini landing page. Same conversion principles apply.",
            static_content=(
                "## Registration Page Essentials\n\n"
                "### What It Needs\n"
                "1. **Headline**: outcome-focused ('Learn how to [result] in [timeframe]')\n"
                "2. **3 bullet takeaways**: what they'll learn (specific, not vague)\n"
                "3. **Speaker credibility**: 1-2 lines of proof\n"
                "4. **Date/time**: with timezone and duration\n"
                "5. **Registration form**: name + email (nothing more)\n"
                "6. **Urgency element**: limited spots, countdown, or registration deadline\n\n"
                "### Show-Up Rate Optimization\n"
                "Average webinar show-up: 30-40% of registrants.\n"
                "To improve:\n"
                "- Reminder at 24h, 1h, and 'starting now'\n"
                "- 'Add to calendar' button in confirmation\n"
                "- Tease specific content: 'I'll share the exact template I use for…'\n"
                "- Keep it under 60 min (45 min ideal)"
            ),
            dynamic_prompt=(
                "Write the registration page copy and reminder sequence.\n\n"
                "Based on:\n"
                "- Topic: derived from {Q7}, {Q35} (the problem they solve)\n"
                "- Target audience: {Q34}\n"
                "- Proof: {Q33}\n"
                "- Messaging from U5\n\n"
                "Produce:\n"
                "1. **Webinar title** (outcome-driven, specific)\n"
                "2. **Registration page copy** (headline, 3 takeaways, speaker bio, CTA)\n"
                "3. **Confirmation email** (full copy + calendar link reminder)\n"
                "4. **24h reminder** (tease content)\n"
                "5. **1h reminder** (link + excitement)\n"
                "6. **Starting now** (direct link)"
            ),
        ),
        SectionSpec(
            name="Full Presentation Script",
            purpose="The complete script from hook to close",
            tone_note="HEAVY model — this is the most complex long-form generation in the system.",
            static_content=(
                "## The Webinar/VSL Structure\n\n"
                "### The 8-Part Framework (60 min total)\n"
                "| Part | Duration | Purpose |\n"
                "|------|----------|--------|\n"
                "| **1. Hook** | 2 min | Grab attention, state the big promise |\n"
                "| **2. Origin Story** | 5 min | Build credibility and relatability |\n"
                "| **3. The Problem** | 8 min | Agitate the pain they're experiencing |\n"
                "| **4. The Mechanism** | 10 min | Explain WHY the problem exists (education) |\n"
                "| **5. The Solution** | 10 min | Your framework/method (the WHAT, not the HOW) |\n"
                "| **6. Case Studies** | 5 min | Proof that the solution works |\n"
                "| **7. The Offer** | 10 min | Present the value stack |\n"
                "| **8. Close & FAQ** | 10 min | Handle objections, create urgency, CTA |\n\n"
                "### Key Principles\n"
                "- **Teach genuinely**: the education portion must deliver real value\n"
                "- **The transition**: 'Now you know WHAT to do. If you want help doing it…'\n"
                "- **Never surprise-sell**: if they didn't expect an offer, they'll feel tricked\n"
                "- **The 60/40 rule**: 60% education, 40% offer + close"
            ),
            dynamic_prompt=(
                "Write the complete 8-part script for this client.\n\n"
                "Using:\n"
                "- Problem: {Q35}, {Q36}\n"
                "- Solution: {Q7}\n"
                "- Proof: {Q33}\n"
                "- Avatar from U2 (pains, outcomes, transformation)\n"
                "- Offer from U3 (value stack, guarantee, naming)\n"
                "- Positioning from U5 (messaging angles)\n\n"
                "For EACH of the 8 parts:\n"
                "1. **Opening line** (the first sentence of this section)\n"
                "2. **Key points** (3-5 bullet points to cover)\n"
                "3. **Transition line** (how to move to the next section)\n"
                "4. **Slide notes** (what should be on screen)\n"
                "5. **Speaker notes** (delivery guidance — tone, pace, emphasis)\n\n"
                "Part 3 (Problem): use the ICP's actual vocabulary from {Q34}, {Q36}.\n"
                "Part 5 (Solution): teach a genuine framework — not a teaser.\n"
                "Part 7 (Offer): follow U3 value stack order exactly.\n"
                "Part 8 (Close): use guarantee from U3, objection rebuttals from BM1 if available."
            ),
        ),
        SectionSpec(
            name="Post-Webinar & Replay Strategy",
            purpose="Convert attendees and non-attendees after the live event",
            tone_note="50%+ of webinar conversions happen AFTER the live event. Don't neglect this.",
            static_content=(
                "## Post-Webinar Conversion\n\n"
                "### For Attendees Who Didn't Buy\n"
                "| When | Email | Purpose |\n"
                "|------|-------|--------|\n"
                "| Same day | Replay link + offer summary | Catch while warm |\n"
                "| Day 2 | FAQ / objection handling | Address hesitation |\n"
                "| Day 4 | Case study deep-dive | More proof |\n"
                "| Day 6 | Deadline reminder | Urgency |\n"
                "| Day 7 | Last chance | Final push |\n\n"
                "### For No-Shows\n"
                "| When | Email | Purpose |\n"
                "|------|-------|--------|\n"
                "| Same day | 'You missed it — here's the replay' | Second chance |\n"
                "| Day 3 | Key takeaway + replay | Value-first re-engagement |\n\n"
                "### Replay Strategy\n"
                "- Make replay available for 5-7 days (not forever — urgency)\n"
                "- Replay page = registration page structure + embedded video\n"
                "- Add CTA overlay or button below video"
            ),
            dynamic_prompt=(
                "Write the complete post-webinar follow-up.\n\n"
                "Produce:\n"
                "1. **5 post-webinar emails for attendees** (full copy for each)\n"
                "2. **2 emails for no-shows** (full copy)\n"
                "3. **Replay page copy** (headline, what they'll learn, CTA)\n"
                "4. **Deadline structure** (when does the offer expire? what changes after?)\n"
                "5. **Conversion metrics to track** (registration rate, show-up, replay views, sales)"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate the COMPLETE script. "
                "This document is an exception to the usual length limit — target 2000 words. "
                "Every section must have full speaker notes in <p> tags, not just <ul> bullets. "
                "All emails must be complete. Use <h2> for the 8 parts, <h3> for sub-sections."
            ),
        ),
        FormatSpec(
            format=Format.SLIDES,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate JSON for a slide deck outline.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "[\n"
                '  {"slide": 1, "section": "Hook", "title": "...", '
                '   "bullets": ["..."], "speaker_notes": "Full script for this slide..."},\n'
                '  {"slide": 2, "section": "Hook", "title": "...", '
                '   "bullets": ["..."], "speaker_notes": "..."}\n'
                "]\n"
                "```\n"
                "Max 3 bullets per slide. Speaker notes = complete talk track.\n"
                "Target: 25-35 slides for a 45-60 min presentation."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q10", "Q16",
        "Q33", "Q34", "Q35", "Q36", "Q37",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5, DocID.BM1],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: "Simpler script. 30-min workshop format instead of full webinar. Less aggressive close.",
        Maturity.GROWING: "Full 60-min webinar. All 8 parts. Moderate close intensity.",
        Maturity.ESTABLISHED: "Premium masterclass positioning. Multiple case studies. Confident close.",
        Maturity.PIVOT: "Teach from old domain expertise, sell new domain service. Bridge narrative.",
    },
    bottleneck_adaptations={
        Bottleneck.CONVERSION: "The webinar IS the conversion tool. Maximum depth on Part 7-8.",
        Bottleneck.VISIBILITY: "Webinar doubles as authority-building content. Emphasize Part 4-5.",
        Bottleneck.LEAD_GENERATION: "Registration page is the lead capture. Promotion strategy matters.",
        Bottleneck.PRICING: "Offer presentation (Part 7) must use U4 anchoring logic.",
        Bottleneck.RETENTION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "Registration page must pre-qualify. 'This is for [specific person].'",
    },
    quality_rules=[
        "Script must be a complete speaker document — not just slides or bullet points.",
        "Education portions (Parts 3-5) must deliver genuine value. No teaser content.",
        "The transition to the offer (Part 6→7) must feel natural, not abrupt.",
        "Slide deck must have max 3 bullets per slide — the script is in speaker notes.",
        "All follow-up emails must be complete copy with subject lines.",
        "Registration page must be a mini landing page — not just a form.",
    ],
)