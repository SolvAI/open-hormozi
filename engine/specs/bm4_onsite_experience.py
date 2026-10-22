"""BM4: On-Site Experience & Upsell.

What happens when the customer walks in or shows up.
Menu engineering, upsell prompts, staff scripts, ambiance.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


BM4_SPEC = DocSpec(
    id=DocID.BM4,
    name="On-Site Experience & Upsell",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Optimize the face-to-face customer experience to increase average transaction value, "
        "satisfaction, and repeat visits. Covers upsell mechanics, staff scripts, "
        "and the physical/sensory experience."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Customer Journey Mapping (On-Site)",
            purpose="Map every touchpoint from arrival to departure",
            tone_note="Specific to business type. A restaurant journey ≠ a salon journey ≠ a retail journey.",
            static_content=(
                "## The On-Site Journey\n\n"
                "Every physical interaction is a sequence of micro-moments. "
                "Each one is a chance to delight or disappoint.\n\n"
                "### Generic Journey Template\n"
                "```\n"
                "Arrival → First Impression → Greeting → Service/Browse → \n"
                "Upsell Moment → Delivery/Purchase → Farewell → Follow-Up Trigger\n"
                "```\n\n"
                "### The 3 Critical Moments\n"
                "1. **First 30 seconds**: greeting, ambiance, cleanliness → sets the emotional tone\n"
                "2. **The upsell moment**: when they're already committed but could add more\n"
                "3. **The farewell**: the last impression determines whether they return\n\n"
                "### Peak-End Rule (Kahneman)\n"
                "People remember the PEAK moment and the END of an experience. "
                "Invest most in making the best part spectacular and the exit warm."
            ),
            dynamic_prompt=(
                "Map the on-site journey for this specific business.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- What they sell/deliver: {Q7}\n"
                "- Physical location type: {Q6}\n\n"
                "Produce:\n"
                "1. **8-12 step journey map** specific to their business\n"
                "   (Restaurant: enter → seated → menu → order → appetizer → main → "
                "   dessert offer → bill → farewell)\n"
                "2. **The peak moment** for their business (what should be the highlight)\n"
                "3. **The farewell ritual** (what happens as they leave)\n"
                "4. **Pain points to eliminate** (common friction in their business type)\n\n"
                "Be very specific to the business type. Don't give a retail journey to a dentist."
            ),
        ),
        SectionSpec(
            name="Upsell & Cross-Sell Strategy",
            purpose="Increase average transaction value through strategic suggestions",
            tone_note="Ethical upselling = genuine recommendations that improve the experience.",
            static_content=(
                "## Ethical Upselling Rules\n\n"
                "Upselling is NOT pushing products people don't want. "
                "It's helping them get more value from their visit.\n\n"
                "### The 3 Upsell Types\n"
                "| Type | What It Is | Example |\n"
                "|------|-----------|--------|\n"
                "| **Upgrade** | Better version of what they chose | 'Our signature version of that has X…' |\n"
                "| **Add-on** | Complementary item | 'Most people also enjoy X with that…' |\n"
                "| **Bundle** | Package deal | 'The combo includes X + Y for only $Z more…' |\n\n"
                "### Upsell Timing\n"
                "- **Before commitment**: upgrades and bundles ('Would you prefer the premium…?')\n"
                "- **After first purchase**: add-ons ('Can I suggest X to go with that?')\n"
                "- **At checkout**: impulse items, next-visit incentive\n\n"
                "### The Language of Suggestion\n"
                "- ✅ 'Our chef recommends…' (authority)\n"
                "- ✅ 'Most customers add…' (social proof)\n"
                "- ✅ 'That pairs beautifully with…' (expertise)\n"
                "- ❌ 'Would you like to add anything else?' (too passive)\n"
                "- ❌ 'Want the large?' (too pushy)"
            ),
            dynamic_prompt=(
                "Design the upsell strategy for this business.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- What they sell: {Q7}\n"
                "- Average transaction: {Q10}\n"
                "- Margin: {Q22}\n\n"
                "Produce:\n"
                "1. **3-5 specific upsell opportunities** for this business\n"
                "   (not generic — 'offer dessert' is generic. "
                "   'After the main course, suggest the house specialty dessert, "
                "   $X, Y% margin' is specific)\n"
                "2. **The exact words** staff should say for each upsell\n"
                "3. **Expected revenue impact**: if upsell rate = 30%, "
                "   average ticket increases by $X → monthly impact = $Y\n"
                "4. **What NOT to upsell** (items that annoy or feel pushy)\n\n"
                "If {Q1} = restaurant: menu engineering — which items to push, which to kill.\n"
                "If {Q1} = salon/spa: service add-ons, product recommendations.\n"
                "If {Q1} = retail: cross-sell complementary products, loyalty card pitch."
            ),
        ),
        SectionSpec(
            name="Staff Scripts & Training Points",
            purpose="Give staff ready-to-use language for every touchpoint",
            tone_note="Printable. These go on the wall of the break room, not in a binder.",
            static_content=(
                "## Why Scripts Matter\n\n"
                "Scripts aren't about turning staff into robots. "
                "They're about setting a MINIMUM quality floor.\n\n"
                "A great employee improvises. A new employee needs a script. "
                "Without scripts, quality depends entirely on who's working that day.\n\n"
                "### Script Design Rules\n"
                "1. Keep each script under 3 sentences\n"
                "2. Use natural language (how a person actually talks)\n"
                "3. Include a fallback ('If they say no, say…')\n"
                "4. Train by role-playing, not reading"
            ),
            dynamic_prompt=(
                "Write the staff scripts for this business.\n\n"
                "Based on the journey map above, write scripts for:\n"
                "1. **Greeting script** (first 30 seconds)\n"
                "2. **Upsell scripts** (one per upsell opportunity identified above)\n"
                "3. **Handling a complaint** (3-step recovery: apologize, fix, bonus)\n"
                "4. **Farewell script** (including rebooking/review ask)\n"
                "5. **Phone inquiry script** (if they call before visiting)\n\n"
                "Each script:\n"
                "- Max 3 sentences\n"
                "- Written as natural speech in English\n"
                "- Includes the fallback if the customer declines\n\n"
                "Format these as a printable cheat sheet (the PNG format will render them)."
            ),
        ),
        SectionSpec(
            name="Ambiance & Physical Optimization",
            purpose="Environmental factors that influence spending and satisfaction",
            tone_note="Specific to business type. A dentist's ambiance ≠ a restaurant's.",
            static_content=(
                "## The Environment Sells\n\n"
                "Research shows:\n"
                "- Slower music → customers spend 15% more time (and more money) in restaurants\n"
                "- Clean restrooms are the #1 factor in restaurant return visits (after food quality)\n"
                "- Warm lighting increases perceived value of products\n"
                "- Scent can increase purchase intent by 80% (Lindström)\n\n"
                "### The 5-Sense Check\n"
                "| Sense | Check | Quick Win |\n"
                "|-------|-------|----------|\n"
                "| Sight | Lighting, cleanliness, signage | Fix lighting first |\n"
                "| Sound | Music volume & genre, noise level | Curated playlist at right volume |\n"
                "| Smell | Fresh, clean, on-brand | Eliminate bad smells first |\n"
                "| Touch | Furniture comfort, temperature | Comfortable seating |\n"
                "| Taste | (if applicable) | Complimentary water/coffee |"
            ),
            dynamic_prompt=(
                "Audit and recommend ambiance improvements for this business.\n\n"
                "Based on:\n"
                "- Business type: {Q1}\n"
                "- Service/product: {Q7}\n"
                "- Target customer: {Q34}\n\n"
                "Run the 5-sense check for their specific business type.\n"
                "For each sense, recommend:\n"
                "1. **Quick win** (costs <$100, implement this week)\n"
                "2. **Medium investment** ($100-500, implement this month)\n"
                "3. **Premium upgrade** ($500+, plan for later)\n\n"
                "If {Q1} = restaurant: focus on music playlist, lighting, table setting.\n"
                "If {Q1} = practitioner: focus on waiting room comfort, anxiety reduction.\n"
                "If {Q1} = retail: focus on product display, flow through the space."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Staff scripts must be written as "
                "natural dialogue in <blockquote> blocks. "
                "Upsell calculations in an HTML <table> with specific numbers."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/bm4_staff_cheat_sheet.html",
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate JSON for a printable A4 staff cheat sheet.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "business_name": "...",\n'
                '  "sections": [\n'
                '    {"title": "Greeting", "script": "...", "if_no": "..."},\n'
                '    {"title": "Upsell: [item]", "script": "...", "if_no": "..."},\n'
                '    {"title": "Complaint", "steps": ["1. ...", "2. ...", "3. ..."]},\n'
                '    {"title": "Farewell", "script": "..."}\n'
                "  ]\n"
                "}\n"
                "```"
            ),
            postprocess="screenshot",
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q6", "Q7", "Q8",
        "Q10", "Q22", "Q34",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: "Focus on the basics: greeting, one upsell, farewell. Don't overwhelm.",
        Maturity.GROWING: "Full journey map. Staff training becomes important as team grows.",
        Maturity.ESTABLISHED: "Refinement. Mystery shopper approach — audit the existing experience.",
        Maturity.PIVOT: "New experience for new business. Apply hospitality principles from day one.",
    },
    bottleneck_adaptations={
        Bottleneck.PRICING: "Upsell strategy is the priority — increase ticket without raising base price.",
        Bottleneck.RETENTION: "Farewell and rebooking scripts are the priority. The exit experience drives repeat visits.",
        Bottleneck.CONVERSION: "First impression and greeting are critical — they're still 'deciding' when they arrive.",
        Bottleneck.VISIBILITY: "Light treatment — they found you. Now deliver.",
        Bottleneck.LEAD_GENERATION: "Standard depth.",
        Bottleneck.WRONG_CLIENTS: "The experience should confirm they're in the right place (or gently redirect).",
    },
    quality_rules=[
        "Scripts must sound like a real human speaking in english, not corporate training material.",
        "Upsell opportunities must include specific revenue impact calculations.",
        "Staff cheat sheet must fit on one printable page. If it doesn't, it won't be used.",
        "Ambiance recommendations must be budget-tiered (quick win / medium / premium).",
        "Every recommendation must be specific to the business type — not generic hospitality advice.",
    ],
)