"""U1: Diagnostic Report — the "prescription" that drives everything downstream.

This document is unique: most of its content comes from the diagnostic pipeline
(meta-variables, triggers, channel scores, flags) rather than pure LLM generation.
The LLM's job is to synthesize these into a readable, actionable narrative.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U1_SPEC = DocSpec(
    id=DocID.U1,
    name="Diagnostic Report",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Synthesize all intake form data into a current-state snapshot. "
        "Identify the primary bottleneck, maturity level, recommended channel, "
        "and recommended funnel shape. This is the 'prescription' that triggers "
        "and shapes every downstream document."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Executive Summary",
            purpose="One-page snapshot: who you are, where you stand, what to do first",
            tone_note="STARTER: encouraging but honest. ESTABLISHED: direct, no hand-holding. SURVIVAL: urgent, compassionate.",
            static_content=None,  # Fully dynamic — unique to every client
            dynamic_prompt=(
                "Write a 200-300 word executive summary for this client.\n"
                "Include: business type ({Q1}), industry ({Q2}), current revenue ({Q18}), "
                "target revenue ({Q40}), timeline ({Q41}), primary bottleneck ({bottleneck}), "
                "primary channel recommendation ({channel}), and the single most important "
                "action they should take in the next 7 days.\n\n"
                "This must feel like a doctor's summary after a checkup — not a report card, "
                "but a clear diagnosis and treatment plan."
            ),
        ),
        SectionSpec(
            name="Current State Assessment",
            purpose="Objective snapshot of where the business stands today",
            tone_note="Factual. Use the client's own numbers. Don't sugarcoat or catastrophize.",
            static_content=(
                "## How We Assess Your Business\n\n"
                "We evaluate 4 dimensions:\n\n"
                "| Dimension | What It Measures | Why It Matters |\n"
                "|-----------|-----------------|----------------|\n"
                "| **Maturity** | Revenue, track record, proof, experience | Determines how aggressive your strategy can be |\n"
                "| **Bottleneck** | Where the funnel leaks most | Determines what to fix first |\n"
                "| **Resources** | Time vs money available for growth | Determines which tactics are realistic |\n"
                "| **Ambition** | Where you want to go, how fast | Determines pacing and investment level |\n\n"
                "Each dimension is derived from your answers, cross-validated for consistency, "
                "and used to calibrate every recommendation that follows."
            ),
            dynamic_prompt=(
                "Present the 4 meta-variables for this client with full rationale:\n"
                "- Maturity: {maturity} — explain WHY based on {Q18}, {Q3}, {Q32}\n"
                "- Bottleneck: {bottleneck} — explain WHY, cross-validate against numbers\n"
                "  (If Q42 = 'don't know', show the derivation logic)\n"
                "- Resources: {resource_profile} — based on {Q44}, {Q45}, {Q46}\n"
                "- Ambition: {ambition_profile} — based on {Q40}, {Q41}, {Q43}\n\n"
                "Include a radar chart description (scores 1-5 per dimension) that the "
                "chart format will visualize.\n\n"
                "Flag any validation issues: revenue sanity ({Q10} × {Q19} vs {Q18}), "
                "budget vs ambition, hard-no conflicts."
            ),
        ),
        SectionSpec(
            name="Bottleneck Analysis",
            purpose="Deep dive into the identified bottleneck with evidence",
            tone_note="Direct. Show the evidence trail. Don't just name the bottleneck — prove it.",
            static_content=(
                "## The Bottleneck Framework\n\n"
                "Every business has ONE primary bottleneck at any given time. "
                "Fixing anything else first is wasted effort.\n\n"
                "```\n"
                "Visibility → Lead Generation → Conversion → Pricing → Retention\n"
                "```\n\n"
                "- **Visibility**: Nobody knows you exist. Fix this before anything else.\n"
                "- **Lead Generation**: People know you but don't raise their hand. "
                "Usually a messaging or channel problem.\n"
                "- **Conversion**: Leads come in but don't buy. Offer, sales process, or trust problem.\n"
                "- **Pricing**: You sell but at too-low margins. Packaging and positioning problem.\n"
                "- **Retention**: Clients buy once and leave. Delivery, follow-up, or offer depth problem.\n"
                "- **Wrong Clients**: You're busy but miserable. Positioning attracts the wrong audience.\n\n"
                "The bottleneck determines which documents in your strategy pack get the MOST depth."
            ),
            dynamic_prompt=(
                "Analyze this client's bottleneck: {bottleneck}\n\n"
                "Evidence from their answers:\n"
                "- Self-identified bottleneck: {Q42}\n"
                "- Current acquisition methods: {Q23}\n"
                "- What hasn't worked: {Q25}\n"
                "- Revenue trend: {Q21}\n"
                "- Client concentration: {Q20}\n\n"
                "If the self-identified bottleneck contradicts the numbers, explain the discrepancy. "
                "Example: they say 'visibility' but have 100+ clients/month — that's not a visibility problem.\n\n"
                "Prescribe the TOP 3 actions for this bottleneck, ranked by impact. "
                "Reference which downstream documents address each action."
            ),
        ),
        SectionSpec(
            name="Channel Recommendation",
            purpose="Present the recommended acquisition channel with scoring rationale",
            tone_note="Decisive. Pick ONE channel. Acknowledge alternatives but be opinionated.",
            static_content=(
                "## Why One Channel?\n\n"
                "Under $1M/year, spreading across multiple channels is the #1 mistake. "
                "Each channel requires different skills, content, and optimization cycles. "
                "Pick one, master it, then expand.\n\n"
                "### The 7 Channels\n"
                "| Channel | Best For | Minimum Budget | Time Required |\n"
                "|---------|----------|---------------|---------------|\n"
                "| SEA (Google Ads) | High-intent search, B2B services | $1,500/mo | Low (once set up) |\n"
                "| Social Ads | Visual products, local B2C, broad B2C | $500/mo | Low-medium |\n"
                "| Cold Outbound | B2B, identifiable targets, high-ticket | $0-200/mo | High |\n"
                "| Organic Content | Expertise-based, long buying cycles | $0 | Very high |\n"
                "| Local SEO | Physical location, 'near me' searches | $0-200/mo | Medium |\n"
                "| Referral & Partnerships | Existing happy clients, complementary businesses | $0 | Medium |\n"
                "| Marketplace | Currently dependent, need to migrate | Varies | Medium |\n"
            ),
            dynamic_prompt=(
                "Present the channel recommendation for this client.\n\n"
                "**Primary channel: {channel}**\n\n"
                "Show the scoring breakdown for all 7 channels (scores will come from diagnostic). "
                "For the recommended channel, explain:\n"
                "1. WHY it's the best fit (positive factors)\n"
                "2. What it will cost ({Q44} budget alignment)\n"
                "3. Expected timeline to first results\n"
                "4. What they need to do in week 1\n\n"
                "For channels eliminated by hard-nos ({Q48}), acknowledge the constraint "
                "and explain the trade-off explicitly — don't pretend the constraint doesn't exist.\n\n"
                "If marketplace dependency exists ({Q26}), include a migration paragraph: "
                "current dependency level, migration timeline, what success looks like."
            ),
        ),
        SectionSpec(
            name="Document Map",
            purpose="Explain which documents were triggered and why",
            tone_note="Transparent. The client should understand what they're getting and why.",
            static_content=None,
            dynamic_prompt=(
                "List all triggered documents ({triggered_doc_list}) grouped by tier.\n"
                "For each, ONE sentence explaining why it was triggered for this specific client.\n"
                "For documents that were NOT triggered, briefly explain why "
                "(e.g., 'BM1 Sales Playbook: not triggered because your customers buy without a conversation').\n\n"
                "End with the recommended reading order (priority order) "
                "and which documents to implement FIRST vs which to save for Month 2-3."
            ),
        ),
        SectionSpec(
            name="Risk Factors & Validation Flags",
            purpose="Surface any inconsistencies or risks detected in the intake",
            tone_note="Honest but constructive. Frame risks as 'things to address' not 'problems'.",
            static_content=None,
            dynamic_prompt=(
                "Present all validation flags detected for this client.\n"
                "For each flag:\n"
                "- What was detected (the inconsistency or risk)\n"
                "- Why it matters\n"
                "- What to do about it (specific action)\n"
                "- Which downstream document addresses it\n\n"
                "If no flags: state that the intake is internally consistent and proceed with confidence.\n\n"
                "If critical flags exist (e.g., zero resources, declining + no proof): "
                "this section should be prominently placed and the recommended action plan adjusted."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "This is the most important document — "
                "it sets the tone for the entire strategy pack. Be thorough but concise. "
                "The client reads this FIRST. Use <h2>/<h3> for sections, <table> for all data grids."
            ),
        ),
        FormatSpec(
            format=Format.MERMAID,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate TWO Mermaid diagrams:\n"
                "1. A flowchart showing the recommended funnel (current state → steps → goal)\n"
                "2. A radar/comparison showing current vs recommended state on 5 dimensions\n\n"
                "Use flowchart TD for the funnel. Keep labels short and jargon-free.\n"
                "Wrap ALL node labels in double quotes."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q2", "Q3", "Q4", "Q5", "Q6",
        "Q10", "Q18", "Q19", "Q20", "Q21", "Q22",
        "Q23", "Q24", "Q25", "Q26", "Q27",
        "Q32", "Q40", "Q41", "Q42", "Q43",
        "Q44", "Q45", "Q46", "Q48", "Q49",
    ],
    upstream_deps=[],  # U1 is the root — no upstream
    downstream_consumers=[
        DocID.U2, DocID.U3, DocID.U4, DocID.U5, DocID.U6,
        DocID.U7, DocID.U8, DocID.U9,
    ],
    maturity_adaptations={
        Maturity.STARTER: (
            "Educational tone. Explain each concept before applying it. "
            "Emphasize quick wins and minimum viable actions. "
            "Don't overwhelm with the full document list — highlight the 5 most important."
        ),
        Maturity.GROWING: (
            "Direct tone. Acknowledge what's working before diagnosing what isn't. "
            "Focus on systematizing informal processes."
        ),
        Maturity.ESTABLISHED: (
            "Strategic tone. Skip basics. Focus on optimization opportunities "
            "and the specific lever that unlocks the next growth stage."
        ),
        Maturity.PIVOT: (
            "Bridging tone. Acknowledge the expertise they bring from their previous domain. "
            "Frame the diagnostic as 'here's how your experience maps to the new context.'"
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Bottleneck section should be longest. Prescribe channel + first 30-day plan.",
        Bottleneck.LEAD_GENERATION: "Emphasize the gap between awareness and action. Usually a messaging problem.",
        Bottleneck.CONVERSION: "Emphasize offer and sales process. Often U3 and BM1 are the priority docs.",
        Bottleneck.PRICING: "Emphasize the revenue-per-client math. U4 is the priority downstream doc.",
        Bottleneck.RETENTION: "Emphasize LTV vs CAC. BM5 is the priority downstream doc.",
        Bottleneck.WRONG_CLIENTS: "Emphasize repositioning. U2 and U5 are the priority downstream docs.",
    },
    quality_rules=[
        "This document is read FIRST — it must build confidence that the system understands the business.",
        "Never be generic. Every sentence should reference specific form answers.",
        "Channel recommendation must be decisive — pick ONE, not 'it depends'.",
        "If validation flags are critical, put Risk Factors BEFORE the channel recommendation.",
        "The document map should make the client excited to read the other docs, not overwhelmed.",
        "Revenue/financial numbers must be presented accurately — don't round $4,200 to '~$5k'.",
    ],
)