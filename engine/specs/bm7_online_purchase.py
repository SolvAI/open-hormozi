"""BM7: Online Purchase Optimization.

For businesses where the customer can buy without talking to anyone:
product page, checkout flow, trust signals, abandoned cart, post-purchase.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


BM7_SPEC = DocSpec(
    id=DocID.BM7,
    name="Online Purchase Optimization",
    tier=Tier.BUSINESS_MODEL,
    purpose=(
        "Optimize the self-serve buying experience: offer/product page structure, "
        "trust signals, checkout friction reduction, abandoned cart recovery, "
        "post-purchase experience, and cross-sell/upsell logic."
    ),
    model_tier=ModelTier.MEDIUM,
    sections=[
        SectionSpec(
            name="Product/Offer Page Structure",
            purpose="Design the page structure that converts browsers to buyers",
            tone_note="E-commerce and digital products have different page structures. Adapt.",
            static_content=(
                "## The Self-Serve Page Must Do Everything a Salesperson Does\n\n"
                "When there's no human in the loop, the page is the salesperson. "
                "It must: attract attention, build trust, present value, handle objections, "
                "and close — in that order.\n\n"
                "### The Conversion Page Framework\n"
                "| Section | Purpose | Length |\n"
                "|---------|---------|--------|\n"
                "| Hero + CTA | Grab attention, state the outcome | 1 screen |\n"
                "| Problem agitation | Why they're here — reflect their pain | 2-3 paragraphs |\n"
                "| Solution introduction | What you offer (not features — outcomes) | 1-2 paragraphs |\n"
                "| Social proof | Reviews, ratings, testimonials, press | As much as you have |\n"
                "| Product details | Specs, ingredients, curriculum, deliverables | Complete |\n"
                "| Trust signals | Guarantee, security badges, return policy | Always visible |\n"
                "| Price + CTA | Clear price, strong button | Prominent |\n"
                "| FAQ | Handle remaining objections | 5-8 questions |\n"
                "| Final CTA | Last chance before they leave | Bottom of page |\n\n"
                "### E-Commerce vs Digital Product vs Booking\n"
                "- **E-commerce**: heavy on photos, reviews, shipping info\n"
                "- **Digital product**: heavy on curriculum/features, proof, guarantee\n"
                "- **Online booking** (local): heavy on availability, location, reviews"
            ),
            dynamic_prompt=(
                "Design the product/offer page structure for this client.\n\n"
                "Based on:\n"
                "- What they sell: {Q7}\n"
                "- Offer type: {Q8}\n"
                "- Deal size: {Q10}\n"
                "- Target customer: {Q34}\n"
                "- Current website: {Q28}\n"
                "- Proof: {Q32}\n\n"
                "Produce:\n"
                "1. **Page wireframe** (ordered section list with content brief for each)\n"
                "2. **Hero copy** (headline + subheadline + CTA button text)\n"
                "3. **Trust signal placement** (what to show and where)\n"
                "4. **Product description approach** (features vs outcomes vs both)\n"
                "5. **FAQ content** (5-8 questions with answers, drawn from {Q36}, {Q37})\n\n"
                "If {Q8} = physical product: prioritize photos, reviews, shipping.\n"
                "If {Q8} = digital product: prioritize curriculum, proof, guarantee.\n"
                "If {Q13} = 'never' + local: this is a booking/reservation page — "
                "prioritize availability, location, reviews."
            ),
        ),
        SectionSpec(
            name="Checkout Flow Optimization",
            purpose="Remove friction between 'add to cart' and 'purchase complete'",
            tone_note="Every extra click loses 5-10% of buyers. Ruthlessly simplify.",
            static_content=(
                "## The Checkout Friction Audit\n\n"
                "Average cart abandonment rate: **70%** (Baymard Institute).\n"
                "Top abandonment reasons:\n"
                "1. Extra costs too high (shipping, taxes) — 48%\n"
                "2. Account creation required — 24%\n"
                "3. Delivery too slow — 22%\n"
                "4. Too long/complicated checkout — 17%\n"
                "5. Didn't trust the site — 18%\n\n"
                "### Friction Reduction Checklist\n"
                "- [ ] Guest checkout available (no forced account creation)\n"
                "- [ ] Total cost visible BEFORE checkout (no surprises)\n"
                "- [ ] Maximum 3 steps to purchase\n"
                "- [ ] Auto-fill enabled (address, payment)\n"
                "- [ ] Multiple payment methods (CB, PayPal, Apple Pay)\n"
                "- [ ] Security badges visible at checkout\n"
                "- [ ] Progress indicator (step 1 of 3)\n"
                "- [ ] Mobile-optimized (60%+ of traffic is mobile)\n"
                "- [ ] Guarantee/return policy visible at checkout\n"
                "- [ ] Save cart for later (email recovery)"
            ),
            dynamic_prompt=(
                "Audit and optimize the checkout flow for this client.\n\n"
                "Based on:\n"
                "- Offer type: {Q8}\n"
                "- Deal size: {Q10}\n"
                "- Current website: {Q28}\n"
                "- Tech comfort: {Q47}\n\n"
                "Produce:\n"
                "1. **Recommended checkout flow** (steps, what's on each screen)\n"
                "2. **Friction audit**: go through the checklist above for their situation\n"
                "3. **Payment methods to enable** (with platform-specific recommendations)\n"
                "4. **Mobile optimization priorities** (what to test first)\n"
                "5. **Trust signals at checkout** (specific to their business)\n\n"
                "If {Q8} = digital product: instant access post-purchase is critical.\n"
                "If {Q8} = physical product: shipping clarity is #1 priority.\n"
                "If online booking: simplify to date/time → contact info → confirm. That's it."
            ),
        ),
        SectionSpec(
            name="Abandoned Cart & Browse Recovery",
            purpose="Recover the 70% who leave without buying",
            tone_note="This is low-hanging fruit with massive ROI. Even a basic email recovers 5-10%.",
            static_content=(
                "## Abandoned Cart Recovery\n\n"
                "### The Recovery Sequence\n"
                "| Timing | Message | Goal |\n"
                "|--------|---------|------|\n"
                "| 1 hour | 'You left something behind' | Reminder (no discount) |\n"
                "| 24 hours | Social proof + urgency | Build trust |\n"
                "| 48-72 hours | Incentive (free shipping, small discount) | Final push |\n\n"
                "### Rules\n"
                "- Don't discount in email 1 — many people just got distracted\n"
                "- Include product image + name + price in every email\n"
                "- One-click return to cart (deep link, not homepage)\n"
                "- Stop after 3 emails — don't spam\n\n"
                "### Browse Abandonment (no cart)\n"
                "If someone viewed a product but didn't add to cart:\n"
                "- Retargeting ad (if budget allows)\n"
                "- Browse abandonment email (if you have their email)"
            ),
            dynamic_prompt=(
                "Design the abandoned cart recovery for this client.\n\n"
                "Based on:\n"
                "- Product type: {Q8}\n"
                "- Deal size: {Q10}\n"
                "- Margin: {Q22}\n\n"
                "Produce:\n"
                "1. **3-email abandoned cart sequence** (full copy for each)\n"
                "   - Email 1: reminder, no discount\n"
                "   - Email 2: social proof or FAQ\n"
                "   - Email 3: incentive (calculate max discount from margin)\n"
                "2. **Subject lines** for each email (A/B versions)\n"
                "3. **Incentive logic**: what discount/bonus is profitable "
                "   given {Q22} margin and {Q10} deal size\n\n"
                "If digital product: no shipping-related recovery. Focus on guarantee and access.\n"
                "If local booking: 'Your reservation wasn't completed' → reschedule CTA."
            ),
        ),
        SectionSpec(
            name="Post-Purchase Experience & Cross-Sell",
            purpose="Turn the purchase into a relationship, not a transaction",
            tone_note="The sale isn't the end — it's the beginning of the retention loop.",
            static_content=(
                "## The Post-Purchase Window\n\n"
                "The 30 minutes after purchase is the peak emotional state: "
                "excitement, anticipation, slight anxiety. Use it.\n\n"
                "### The Post-Purchase Sequence\n"
                "| When | What | Purpose |\n"
                "|------|------|--------|\n"
                "| Immediately | Confirmation + next steps | Reduce anxiety |\n"
                "| Within 1 hour | 'Getting started' or shipping update | Speed to first value |\n"
                "| Day 3-5 | Check-in / usage tips | Increase engagement |\n"
                "| Day 7-14 | Cross-sell / upsell | Extend relationship |\n"
                "| Day 14-21 | Review request | Build social proof |\n\n"
                "### Cross-Sell Logic\n"
                "- **Complementary**: bought a camera → offer a lens\n"
                "- **Consumable**: bought a printer → offer ink (timed to usage)\n"
                "- **Upgrade**: using the basic plan → show premium features\n"
                "- **Frequency**: bought once → offer subscription/bundle"
            ),
            dynamic_prompt=(
                "Design the post-purchase experience for this client.\n\n"
                "Based on:\n"
                "- Product/service: {Q7}, {Q8}\n"
                "- Repeat potential: {Q11}\n"
                "- Deal size: {Q10}\n\n"
                "Produce:\n"
                "1. **Confirmation page content** (what they see right after purchase)\n"
                "2. **Confirmation email** (full copy)\n"
                "3. **Cross-sell / upsell recommendations** specific to their products\n"
                "4. **Timing logic**: when to present cross-sells (immediately vs delayed)\n"
                "5. **Review request approach** (timing + channel + copy)\n\n"
                "If {Q8} = physical product: shipping updates are critical.\n"
                "If {Q8} = digital: instant access is critical — no 'wait for our team to activate.'\n"
                "If {Q11} = repeat: post-purchase must feed into BM5 retention loop."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "All email copy must be complete. "
                "Page wireframe should be a detailed ordered list with content notes per section."
            ),
        ),
        FormatSpec(
            format=Format.PNG,
            method=GenerationMethod.LLM_THEN_RENDER,
            template_path="templates/html/bm7_page_wireframe.html",
            model_tier=ModelTier.HEAVY,
            prompt_fragment=(
                "Generate JSON for an annotated product page wireframe.\n"
                "Return ONLY valid JSON:\n"
                "```json\n"
                "{\n"
                '  "page_type": "e-commerce | digital | booking",\n'
                '  "sections": [\n'
                '    {"name": "Hero", "content_brief": "...", "height_hint": "tall"},\n'
                '    {"name": "Social Proof", "content_brief": "...", "height_hint": "medium"},\n'
                '    {"name": "Product Details", "content_brief": "...", "height_hint": "tall"},\n'
                '    {"name": "CTA", "content_brief": "...", "height_hint": "short"}\n'
                "  ]\n"
                "}\n"
                "```"
            ),
            postprocess="screenshot",
        ),
        FormatSpec(
            format=Format.HTML,
            method=GenerationMethod.STATIC,
            template_path="templates/html/bm7_page_audit_checklist.html",
        ),
    ],
    relevant_questions=[
        "Q1", "Q7", "Q8", "Q10", "Q11", "Q13",
        "Q22", "Q28", "Q32", "Q34", "Q36", "Q37",
        "Q47",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.FC4],
    maturity_adaptations={
        Maturity.STARTER: (
            "Build the basics: one good product page, clean checkout, confirmation email. "
            "Abandoned cart can wait until there's traffic."
        ),
        Maturity.GROWING: (
            "Full optimization. Abandoned cart, cross-sell, post-purchase sequence. "
            "They have traffic but leak at checkout."
        ),
        Maturity.ESTABLISHED: (
            "Advanced: A/B test page elements, dynamic cross-sell, sophisticated "
            "abandoned cart with segmentation."
        ),
        Maturity.PIVOT: "New product page for new offering. Apply e-commerce best practices from day one.",
    },
    bottleneck_adaptations={
        Bottleneck.CONVERSION: (
            "THIS IS THE PRIORITY. If they get traffic but no sales, the page is broken. "
            "Full depth on page structure, trust signals, and checkout friction."
        ),
        Bottleneck.PRICING: "Page must present price in the context of value. Connect to U3/U4.",
        Bottleneck.RETENTION: "Post-purchase experience and cross-sell are the priority sections.",
        Bottleneck.VISIBILITY: "Standard depth — the page needs to exist before it needs traffic.",
        Bottleneck.LEAD_GENERATION: "Page may need a lead capture alternative for non-buyers.",
        Bottleneck.WRONG_CLIENTS: "Page copy must pre-qualify — 'This is for people who...'",
    },
    quality_rules=[
        "Page wireframe must be specific enough that a developer/designer can implement it.",
        "Abandoned cart emails must include product image, name, price, and one-click return link.",
        "Trust signals must be real — don't recommend fake badges or manufactured reviews.",
        "Checkout flow must have 3 steps or fewer. No exceptions for Phase 1.",
        "Cross-sell recommendations must be genuinely useful, not just 'more expensive items'.",
        "Post-purchase confirmation must include IMMEDIATE next steps — no 'we'll get back to you.'",
        "All copy must be in English, matching U5 tone guidelines.",
    ],
)