"""MT3: Automation & Tech Stack Guide.

Tool recommendations, minimum viable stack, setup checklists,
and automation recipes for solo operators and small teams.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


MT3_SPEC = DocSpec(
    id=DocID.MT3,
    name="Automation & Tech Stack Guide",
    tier=Tier.MATURITY,
    purpose=(
        "Recommend the complete tool stack for this client's funnel: forms, automation, "
        "email, scheduling, CRM, and tracking. 'Minimum viable stack' vs 'ideal stack' "
        "with cost breakdown, setup checklist, and automation recipes."
    ),
    model_tier=ModelTier.HEAVY,
    sections=[
        SectionSpec(
            name="Stack Architecture",
            purpose="Show how tools connect to form the complete system",
            tone_note="Match complexity to their tech level. A spreadsheet IS a CRM for someone with 5 clients.",
            static_content=(
                "## The Tool Stack Layers\n\n"
                "```\n"
                "┌─────────────────────────────────────────┐\n"
                "│  ACQUISITION        (how leads find you) │\n"
                "│  Ads / SEO / Outreach / Social           │\n"
                "├─────────────────────────────────────────┤\n"
                "│  CAPTURE             (how you catch them) │\n"
                "│  LP builder / Forms / Booking tool        │\n"
                "├─────────────────────────────────────────┤\n"
                "│  NURTURE            (how you follow up)   │\n"
                "│  Email tool / CRM / Automation            │\n"
                "├─────────────────────────────────────────┤\n"
                "│  CONVERT               (how they buy)     │\n"
                "│  Checkout / Proposals / Scheduling         │\n"
                "├─────────────────────────────────────────┤\n"
                "│  DELIVER             (how you serve them) │\n"
                "│  Project mgmt / Communication / Docs      │\n"
                "├─────────────────────────────────────────┤\n"
                "│  TRACK               (how you measure)    │\n"
                "│  Analytics / Dashboards / Spreadsheets     │\n"
                "└─────────────────────────────────────────┘\n"
                "```\n\n"
                "### The 3 Stack Levels\n"
                "| Level | Monthly Cost | Tools | Best For |\n"
                "|-------|-------------|-------|----------|\n"
                "| **Minimum Viable** | $0-50/mo | Free tiers + spreadsheets | Pre-revenue, solo, testing |\n"
                "| **Growth** | $50-200/mo | Paid tiers + basic automation | $5-20k/mo revenue |\n"
                "| **Scale** | $200-500/mo | Full CRM + advanced automation | $20k+/mo, team of 3+ |"
            ),
            dynamic_prompt=(
                "Design the stack architecture for this client.\n\n"
                "Based on:\n"
                "- Channel: {channel}\n"
                "- Triggered docs: {triggered_doc_list} (each implies tools)\n"
                "- Budget: {Q44}\n"
                "- Tech comfort: {Q47}\n"
                "- Team size: {Q4}\n"
                "- Current tools: {Q28} (website), {Q30} (email), {Q31} (social)\n\n"
                "Produce:\n"
                "1. **Recommended stack level** (minimum / growth / scale) with rationale\n"
                "2. **Architecture diagram** description (what connects to what)\n"
                "3. **Upgrade path**: 'Start with X. When you reach [milestone], upgrade to Y.'\n\n"
                "If {Q47} = 'none of the above': minimum viable only. "
                "Don't recommend HubSpot to someone who can't set up a form."
            ),
        ),
        SectionSpec(
            name="Tool Recommendations Per Layer",
            purpose="Specific tool for each function, with alternatives and pricing",
            tone_note="Opinionated. Don't list 10 options — pick one and explain why.",
            static_content=(
                "## Tool Selection Criteria\n\n"
                "For each tool, evaluate:\n"
                "1. **Does it do the ONE thing I need?** (not the most features)\n"
                "2. **Can I set it up in < 2 hours?** (complexity kills adoption)\n"
                "3. **Does it connect to my other tools?** (via Zapier/Make or native)\n"
                "4. **Can I afford it for 6+ months?** (tool-hopping wastes time)\n"
                "5. **Does it have adequate support and documentation?**\n\n"
                "### The Integration Rule\n"
                "Two connected tools > one all-in-one that does everything poorly. "
                "BUT: too many tools creates chaos. Sweet spot: 4-6 core tools.\n\n"
                "### Common Stacks by Business Type\n"
                "| Business | Capture | Nurture | Convert | Track |\n"
                "|----------|---------|---------|---------|-------|\n"
                "| Freelancer/Consultant | Carrd + Calendly | Mailchimp/ConvertKit | Notion + Google Docs | GA4 + Sheets |\n"
                "| Local Business | WordPress + Google Forms | Mailchimp | Stripe/Square | GA4 + GBP Insights |\n"
                "| E-commerce | Shopify | Klaviyo | Shopify Checkout | Shopify Analytics |\n"
                "| Coach/Course Creator | Systeme.io/Kajabi | Built-in email | Stripe | Built-in analytics |"
            ),
            dynamic_prompt=(
                "Recommend specific tools for each layer.\n\n"
                "For each of the 6 layers (Acquisition, Capture, Nurture, Convert, Deliver, Track):\n"
                "1. **Recommended tool** (one primary recommendation)\n"
                "2. **Why this tool** (specific to their situation)\n"
                "3. **Alternative** (if the primary doesn't fit)\n"
                "4. **Pricing** (free tier + paid tier if relevant)\n"
                "5. **Setup difficulty** (easy / medium / hard)\n\n"
                "Present as a comparison table:\n"
                "| Layer | Tool | Cost | Setup | Why |\n\n"
                "Then provide the total monthly cost:\n"
                "- Minimum viable: $X/mo total\n"
                "- Growth: $Y/mo total\n\n"
                "Match to their budget ({Q44}) and tech comfort ({Q47})."
            ),
        ),
        SectionSpec(
            name="Automation Recipes",
            purpose="Specific automation workflows for their funnel",
            tone_note="Ready to implement. Not 'you could automate X' but 'here's the Zapier recipe.'",
            static_content=(
                "## Automation Priority Matrix\n\n"
                "| Automation | Time Saved | Setup Time | Priority |\n"
                "|-----------|-----------|-----------|----------|\n"
                "| New lead → email notification + CRM entry | 10 min/lead | 30 min | Critical |\n"
                "| Form submit → confirmation email | 5 min/lead | 15 min | Critical |\n"
                "| Appointment booked → reminder sequence | 5 min/booking | 30 min | High |\n"
                "| No-show → recovery email | 5 min/no-show | 20 min | High |\n"
                "| New client → onboarding sequence | 15 min/client | 45 min | Medium |\n"
                "| Invoice paid → thank you email | 3 min/payment | 15 min | Low |\n\n"
                "### Zapier vs Make vs Native\n"
                "- **Native integrations** (tool A talks to tool B directly): best, use first\n"
                "- **Zapier**: easiest, limited free tier (5 zaps), ~$20/mo for more\n"
                "- **Make (Integromat)**: more powerful, better free tier, steeper learning curve\n"
                "- **n8n**: self-hosted, free, requires technical setup\n\n"
                "### The 80/20 Rule\n"
                "Automate the 3-4 workflows that save the most time. "
                "Don't spend 10 hours automating something that takes 2 minutes."
            ),
            dynamic_prompt=(
                "Design the automation recipes for this client's funnel.\n\n"
                "Based on:\n"
                "- Funnel from U6\n"
                "- Triggered docs (each implies automations)\n"
                "- Tech comfort: {Q47}\n"
                "- Time available: {Q45}\n\n"
                "For each automation recipe:\n"
                "1. **Name** (e.g., 'New Lead → CRM + Email')\n"
                "2. **Trigger**: what starts it (form submit, calendar booking, payment…)\n"
                "3. **Actions**: step-by-step what happens (in order)\n"
                "4. **Tools involved**: which tools connect\n"
                "5. **Integration method**: native / Zapier / Make\n"
                "6. **Setup time estimate**\n"
                "7. **Setup steps**: 3-5 concrete steps to configure it\n\n"
                "Prioritize by time saved. Mark critical automations that should be set up "
                "in Week 1-2 of the launch roadmap.\n\n"
                "If {Q47} = 'none of the above': max 2 automations, use simplest tools. "
                "The rest stays manual until they're comfortable."
            ),
        ),
        SectionSpec(
            name="CRM Pipeline & Setup",
            purpose="Configure the CRM pipeline that matches their sales process",
            tone_note="A CRM is only useful if it's used. For 5 clients, a spreadsheet IS the CRM.",
            static_content=(
                "## CRM: What You Actually Need\n\n"
                "### The Pipeline Stages\n"
                "Every business needs these stages (named differently per context):\n"
                "1. **New lead** (just arrived, not yet contacted)\n"
                "2. **Contacted** (first outreach or response)\n"
                "3. **Qualified** (meets criteria, worth pursuing)\n"
                "4. **Proposal sent** (offer presented)\n"
                "5. **Closed won** (they bought)\n"
                "6. **Closed lost** (they didn't — track the reason)\n\n"
                "### CRM Options by Complexity\n"
                "| Tool | Cost | Best For | Limit |\n"
                "|------|------|----------|-------|\n"
                "| **Google Sheets** | Free | 1-20 active leads | No automation |\n"
                "| **Notion** | Free-$10 | 1-30 leads + project mgmt | Manual |\n"
                "| **HubSpot Free** | Free | 30-100 leads | Limited automation |\n"
                "| **Pipedrive** | ~$15/mo | Sales-focused teams | Full pipeline |\n"
                "| **Brevo (CRM)** | Free-$25 | Email + CRM combo | Integrated |\n\n"
                "### The Adoption Test\n"
                "Will you actually update it every day? If not, use something simpler. "
                "An empty CRM is worse than a spreadsheet you actually maintain."
            ),
            dynamic_prompt=(
                "Design the CRM setup for this client.\n\n"
                "Based on:\n"
                "- Client volume: {Q19}\n"
                "- Sales process: {Q13}, {Q16}\n"
                "- Team size: {Q4}\n"
                "- Tech comfort: {Q47}\n\n"
                "Produce:\n"
                "1. **Recommended CRM tool** with rationale\n"
                "2. **Pipeline stages** customized to their sales process\n"
                "   (use their business language, not generic stages)\n"
                "3. **Custom fields** to add (deal size, source, next action)\n"
                "4. **Setup checklist**: step-by-step to get the CRM working\n"
                "5. **Daily CRM routine** (2-5 minutes — what to update)\n\n"
                "If {Q19} ≤ 10 clients/mo AND {Q4} = solo: recommend Google Sheets or Notion. "
                "A full CRM is overkill and they won't use it."
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Format tool comparisons as HTML <table> elements. "
                "Automation recipes as <ol> with <li> steps. "
                "Cost totals in a <div class=\"metric-row\"> with metric cards.\n\n"
                "For each recommended tool, include a link using this format:\n"
                '  <a href="https://www.google.com/search?q=getapp.com+TOOL_NAME">Tool Name</a>\n'
                "Replace TOOL_NAME with the URL-encoded tool name."
            ),
        ),
        FormatSpec(
            format=Format.MERMAID,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MEDIUM,
            prompt_fragment=(
                "Generate a Mermaid flowchart showing the tool architecture.\n"
                "Nodes = tools. Arrows = data flow between tools.\n"
                "Group by layer using subgraphs (Capture, Nurture, Convert, Track).\n"
                "Label arrows with what data passes between tools.\n"
                "Quote all labels. Max 15 nodes."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q13", "Q16", "Q19",
        "Q28", "Q30", "Q31",
        "Q44", "Q45", "Q46", "Q47",
    ],
    upstream_deps=[DocID.U6, DocID.U8],
    downstream_consumers=[],  # MT3 is terminal — supports execution, doesn't feed other docs
    maturity_adaptations={
        Maturity.STARTER: (
            "Minimum viable stack ONLY. Free tools. Spreadsheet CRM. "
            "1-2 automations max. Don't let tool setup delay launching."
        ),
        Maturity.GROWING: (
            "Growth stack. Paid email tool, basic CRM, 3-5 automations. "
            "The upgrade from spreadsheet to CRM happens here."
        ),
        Maturity.ESTABLISHED: (
            "Optimize and consolidate. They may have too many tools. "
            "Simplify, integrate, automate more aggressively."
        ),
        Maturity.PIVOT: (
            "New stack for new business. Can leverage old tech skills but "
            "choose tools appropriate for the new domain."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Focus on acquisition and tracking tools. CRM is secondary.",
        Bottleneck.LEAD_GENERATION: "Focus on capture tools (forms, LP builders) and email automation.",
        Bottleneck.CONVERSION: "CRM pipeline is the priority. Proposal tools, follow-up automation.",
        Bottleneck.PRICING: "Standard depth. Maybe a pricing calculator tool recommendation.",
        Bottleneck.RETENTION: "Focus on email automation for retention sequences.",
        Bottleneck.WRONG_CLIENTS: "CRM tagging to track client quality. Qualification form tools.",
    },
    quality_rules=[
        "Tool recommendations must include specific pricing (free tier + paid).",
        "Never recommend more than 6-8 tools total. More = adoption failure.",
        "Automation recipes must have step-by-step setup instructions, not just descriptions.",
        "CRM recommendation must pass the adoption test — will they actually use it?",
        "Cost totals must be explicit: 'Your minimum viable stack = $X/mo total.'",
        "For tech-uncomfortable clients (Q47), every tool must have a 'setup in under 1 hour' path.",
        "Don't recommend tools the client said they can't use (cross-reference Q47).",
    ],
)