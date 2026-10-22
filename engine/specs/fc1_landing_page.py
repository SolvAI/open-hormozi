"""FC1: Landing Page.

Wireframe, full copy, legal compliance, and optional coded template
for the primary conversion page in the funnel.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


FC1_SPEC = DocSpec(
    id=DocID.FC1,
    name="Landing Page",
    tier=Tier.FUNNEL,
    purpose=(
        "Design a complete landing page: section-by-section wireframe, full conversion copy, "
        "CTA strategy, legal compliance (CGV, RGPD, guarantee terms), "
        "and platform recommendation. Ready to build or hand to a developer."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Page Strategy & Structure",
            purpose="Define the page type, goal, and section order",
            tone_note="The LP is the funnel's hinge. Every element must serve the ONE conversion goal.",
            static_content=(
                "## Landing Page Principles\n\n"
                "### The ONE Rule\n"
                "One page. One offer. One CTA. One audience.\n"
                "If you're tempted to add a navigation menu, a second offer, "
                "or links to other pages — don't. Every exit is a lost conversion.\n\n"
                "### Page Types\n"
                "| Type | Goal | Length | Best For |\n"
                "|------|------|--------|----------|\n"
                "| **Lead capture** | Collect email/phone | Short (1-2 screens) | Lead magnet, free consultation |\n"
                "| **Sales page** | Direct purchase | Long (full value stack) | Products, courses, programs |\n"
                "| **Application** | Qualify + book call | Medium (3-5 screens) | High-ticket services |\n"
                "| **Local** | Visit/call/reserve | Short-Medium | Restaurant, practice, local service |\n\n"
                "### The Conversion Section Order\n"
                "```\n"
                "1. Hero (headline + subheadline + CTA)\n"
                "2. Problem agitation\n"
                "3. Solution introduction\n"
                "4. Value stack / offer details\n"
                "5. Social proof (testimonials, logos, results)\n"
                "6. Guarantee\n"
                "7. FAQ (objection handling)\n"
                "8. Final CTA\n"
                "```\n"
                "Not every page needs all 8. Short pages skip 2-4. Long pages expand each."
            ),
            dynamic_prompt=(
                "Define the LP strategy for this client.\n\n"
                "Based on:\n"
                "- Channel: {channel} (determines traffic source + intent level)\n"
                "- Conversation required: {Q13}\n"
                "- Deal size: {Q10}\n"
                "- Offer type: {Q8}\n"
                "- Physical location: {Q6}\n"
                "- Current website: {Q28}\n\n"
                "Determine:\n"
                "1. **Page type** (lead capture / sales / application / local)\n"
                "2. **Primary conversion action** (the ONE thing they should do)\n"
                "3. **Section order** (which of the 8 sections to include, in what order)\n"
                "4. **Page length estimate** (short/medium/long)\n"
                "5. **Platform recommendation** (Carrd, Webflow, WordPress, Squarespace…) "
                "matched to {Q47} tech comfort and {Q44} budget"
            ),
        ),
        SectionSpec(
            name="Section-by-Section Copy",
            purpose="Complete copy for every section of the landing page",
            tone_note="This is the deliverable. Full copy, not 'write something about your benefits.'",
            static_content=(
                "## Copy Writing Rules for Landing Pages\n\n"
                "1. **Above the fold**: visitor must understand WHAT, WHO, and WHY in 5 seconds\n"
                "2. **Headlines**: benefit-first, specific, urgent\n"
                "3. **Body copy**: short paragraphs (2-3 lines), active voice, you > we\n"
                "4. **Social proof**: specific numbers > vague praise\n"
                "   - ❌ 'Thomas is great to work with!'\n"
                "   - ✅ 'Thomas delivered our MVP in 6 weeks. We raised $2M three months later.'\n"
                "5. **CTA buttons**: action verb + outcome\n"
                "   - ❌ 'Submit' / 'Learn More'\n"
                "   - ✅ 'Book My Free Strategy Session' / 'Get My Growth Plan'\n"
                "6. **FAQ**: every FAQ answer should END by reinforcing the CTA\n\n"
                "### Mobile First\n"
                "60%+ of LP traffic is mobile. Write for a 4-inch screen first."
            ),
            dynamic_prompt=(
                "Write the complete landing page copy.\n\n"
                "Using:\n"
                "- Positioning from U5 (messaging angles, headlines, vocabulary)\n"
                "- Offer from U3 (value stack, guarantee, naming)\n"
                "- Avatar from U2 (pains, outcomes, transformation grid)\n"
                "- Pricing from U4 (if applicable to this page type)\n"
                "- Proof from {Q33}\n\n"
                "For EACH section in the wireframe:\n"
                "1. **Section name**\n"
                "2. **Purpose** (what this section accomplishes)\n"
                "3. **Full copy** (every word — headline, body, bullets, CTA)\n"
                "4. **Visual direction** (what image/element accompanies the text)\n\n"
                "Sections to write (adapt based on page type):\n"
                "- **Hero**: headline + subheadline + CTA + supporting visual\n"
                "- **Problem**: agitate the pain using language from U2\n"
                "- **Solution**: introduce the offer (outcome-first, not feature-first)\n"
                "- **Value stack**: from U3 (core + bonuses with names and anchored values)\n"
                "- **Social proof**: case studies from {Q33}, testimonial format\n"
                "- **Guarantee**: from U3 guarantee design\n"
                "- **FAQ**: 5-8 questions that handle buying objections\n"
                "- **Final CTA**: urgency-enhanced repeat of the primary CTA\n\n"
                "Write in English. Match U5 tone guidelines exactly."
            ),
        ),
        SectionSpec(
            name="Legal Compliance",
            purpose="Privacy law, terms of sale, and guarantee legal framing for the landing page",
            tone_note="Non-negotiable. A LP collecting data without privacy compliance is illegal.",
            static_content=(
                "## Landing Page Legal Requirements\n\n"
                "### Privacy & Data Collection\n"
                "If the page collects ANY personal data (name, email, phone):\n"
                "- [ ] **Consent mechanism** (checkbox or clear notice, per jurisdiction requirements)\n"
                "- [ ] **Privacy policy link**: what data you collect, why, how long you keep it, how to delete\n"
                "- [ ] **Cookie consent banner** (if using analytics/pixels — required in EU, recommended everywhere)\n"
                "- [ ] **Data controller identification**: your name/company, contact\n\n"
                "### Legal Disclosures\n"
                "Required on most commercial websites (varies by jurisdiction):\n"
                "- Business identity (name, address, registration number)\n"
                "- Hosting provider info (required in some jurisdictions)\n"
                "- Contact information\n\n"
                "### Terms of Sale (if selling directly from the page)\n"
                "- Right of withdrawal/return policy (per applicable consumer protection law)\n"
                "- Delivery terms and timing\n"
                "- Payment methods\n"
                "- Guarantee terms (matching U3)\n"
                "- Dispute resolution\n\n"
                "### Claims & Guarantees\n"
                "- Income/result claims require 'results not typical' disclaimer\n"
                "- Professional diligence framing for service businesses\n"
                "- Guarantee terms must match terms of sale exactly\n\n"
                "⚠ This is a framework. Have a legal professional in your jurisdiction review your specific page."
            ),
            dynamic_prompt=(
                "Build the legal compliance elements for this landing page.\n\n"
                "Based on:\n"
                "- What data is collected (from the conversion action defined above)\n"
                "- Offer type: {Q8}\n"
                "- Guarantee from U3\n\n"
                "Produce:\n"
                "1. **Consent/notice text** for data collection (ready to use)\n"
                "2. **Privacy policy outline** (key sections for their specific data collection)\n"
                "3. **Cookie consent text** (if analytics/pixels are used)\n"
                "4. **Legal disclosures** template (fill-in-the-blank for their info)\n"
                "5. **Guarantee disclaimer text** (legal framing of the U3 guarantee)\n"
                "6. **Terms of sale key clauses** if selling directly (returns, delivery, disputes)\n\n"
                "If not selling directly (lead capture only): terms of sale not required, "
                "but privacy compliance and legal disclosures still are."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate the complete LP copy. "
                "Every section must have FULL copy — no placeholders. "
                "Legal elements must be complete texts ready to use."
            ),
        ),
        FormatSpec(
            format=Format.HTML,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate a complete, self-contained HTML landing page: one file, "
                "inline <style>, no build step, deployable as-is on simple hosting.\n"
                "All copy filled in — no lorem, no placeholders except the legal "
                "identity fields the client must supply ([Raison sociale], SIRET…).\n"
                "\n"
                "== DESIGN DIRECTION (decide before writing any CSS) ==\n"
                "Design this page for THIS business, not as a generic template. "
                "First choose, in one line each: (a) the visual world the business "
                "actually belongs to — its materials, tools, documents, vernacular; "
                "(b) a palette of 5-6 hex values named as CSS variables; (c) a type "
                "pairing; (d) ONE signature element the page is remembered by, drawn "
                "from the offer itself (a dated delivery spine, a price/ROI ledger, a "
                "before/after diptych, a specimen grid…). Then build to that decision.\n"
                "\n"
                "== TYPOGRAPHY ==\n"
                "Load fonts from Google Fonts. Use a DISPLAY face for headings that is "
                "NOT the body face, a readable BODY face, and — where the offer has "
                "dates, prices or specs — a MONO face for that data. Do not set the "
                "whole page in Inter or system-ui. Pick the pairing to fit the business "
                "(e.g. Fraunces/Bricolage Grotesque/Space Grotesk/Archivo/Libre "
                "Franklin/Source Serif 4/IBM Plex Sans/IBM Plex Mono/JetBrains Mono).\n"
                "Set a real scale: h1 clamp() around 2.1-3.5rem with tight negative "
                "letter-spacing, body 16-17px, line-height ~1.6, measure capped at "
                "60-70ch. Headline must not run the full page width.\n"
                "\n"
                "== LAYOUT ==\n"
                "Use at least THREE structurally different section layouts. Vertical "
                "rhythm must vary — do not give every section identical padding. "
                "Alternate surfaces (light / tinted / one dark anchor section) so the "
                "page has movement. Prefer a real grid: an annotation rail, an "
                "asymmetric split, a comparison pair or a spec table beats another "
                "centred paragraph.\n"
                "\n"
                "== SECTIONS ==\n"
                "Hero (promise + proof-of-risk-reversal + primary CTA), problem, "
                "solution, delivery/how-it-works, offer & price, differentiation or "
                "proof, guarantee, FAQ, capture form, legal footer.\n"
                "Money and dates are the most persuasive content: set them in the mono "
                "face, right-align figures in tables, and show anchor value vs actual "
                "price rather than a bare number.\n"
                "\n"
                "== QUALITY FLOOR ==\n"
                "Responsive to 360px with no horizontal scroll; visible :focus-visible "
                "outlines; a @media (prefers-reduced-motion: reduce) block; semantic "
                "landmarks; labelled form fields; sufficient contrast on every surface. "
                "Keep CSS selector specificity flat and consistent so section paddings "
                "and backgrounds do not cancel each other out.\n"
                "Include an RGPD consent checkbox on any form.\n"
                "\n"
                "== DO NOT ==\n"
                "No single centred ~760px column for the whole page. No uniform section "
                "padding. No emoji as icons. No unexplained gradient blobs, glassmorphism "
                "or drop-shadow stacks. No generic SaaS blue-violet, and no accent colour "
                "applied to everything — spend the accent on one job (the dated/priced "
                "commitments) and keep the rest quiet. No 01/02/03 numbering unless the "
                "content genuinely is an ordered sequence."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q6", "Q7", "Q8", "Q10", "Q13",
        "Q28", "Q29", "Q32", "Q33", "Q34", "Q35", "Q36",
        "Q44", "Q47",
    ],
    upstream_deps=[DocID.U2, DocID.U3, DocID.U4, DocID.U5],
    downstream_consumers=[DocID.U6, DocID.U8],
    maturity_adaptations={
        Maturity.STARTER: (
            "Simple page. Lead capture or application type. Don't over-design. "
            "Recommend Carrd or single-page builders. Get it live fast."
        ),
        Maturity.GROWING: (
            "Full conversion page. All 8 sections. Integrate proof. "
            "A/B test headline after 2 weeks of data."
        ),
        Maturity.ESTABLISHED: (
            "Premium design. Custom-built or Webflow. "
            "Multiple proof types (case studies, logos, video testimonials)."
        ),
        Maturity.PIVOT: (
            "New page for new offer. Bridge old authority (mention previous domain) "
            "while presenting the new positioning."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Standard page — they need traffic before they need conversion optimization.",
        Bottleneck.LEAD_GENERATION: "THIS IS THE PRIORITY. The LP is where leads are captured.",
        Bottleneck.CONVERSION: "Deep optimization. A/B test sections. Add more proof and objection handling.",
        Bottleneck.PRICING: "Price presentation section is critical. Use U4 anchoring logic.",
        Bottleneck.RETENTION: "Standard depth. LP is an acquisition tool.",
        Bottleneck.WRONG_CLIENTS: "LP must pre-qualify. 'Who this is for' and 'Who this is NOT for' sections.",
    },
    quality_rules=[
        "Every section must have COMPLETE copy. No 'insert your headline here.'",
        "CTA button text must be action + outcome, never 'Submit' or 'Learn More.'",
        "FAQ must handle real buying objections, not filler questions.",
        "Legal compliance section is mandatory. Privacy consent for any data collection.",
        "Social proof must use real results from Q33 — don't fabricate testimonials.",
        "Mobile layout must be considered — no copy that only works on desktop.",
        "The HTML format must be deployable as-is. Self-contained, no external dependencies beyond CDN fonts.",
    ],
)