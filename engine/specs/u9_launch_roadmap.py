"""U9: Launch Roadmap.

Week-by-week implementation plan with milestones, dependencies,
and clear 'done' criteria.
"""

from engine.models.enums import DocID, Format, GenerationMethod, Tier, Maturity, Bottleneck, ModelTier
from engine.models.registry import DocSpec, SectionSpec, FormatSpec


U9_SPEC = DocSpec(
    id=DocID.U9,
    name="Launch Roadmap",
    tier=Tier.UNIVERSAL,
    purpose=(
        "Translate the entire strategy into a week-by-week implementation plan. "
        "6-8 weeks of specific tasks with milestones, dependencies, 'done' criteria, "
        "and Month 2-3 optimization triggers."
    ),
    model_tier=ModelTier.MAX,
    sections=[
        SectionSpec(
            name="Phase Overview",
            purpose="High-level view of the 3 launch phases",
            tone_note="SURVIVAL: compress to 4 weeks. LIFESTYLE: can stretch to 10. GROWTH: standard 6-8.",
            static_content=(
                "## The 3-Phase Launch\n\n"
                "### Phase 1: Foundation (Weeks 1-2)\n"
                "Build the assets. Nothing goes live yet.\n"
                "- Offer finalized (U3/U4)\n"
                "- Positioning locked (U5)\n"
                "- Landing page / key asset created (FC1)\n"
                "- Tracking set up (U8)\n"
                "- Proof assembled (MT1/MT2)\n\n"
                "### Phase 2: Launch (Weeks 3-5)\n"
                "Go live. Start driving traffic.\n"
                "- Primary channel activated\n"
                "- First leads/customers arriving\n"
                "- Daily/weekly monitoring begins\n"
                "- Quick iteration on what's not working\n\n"
                "### Phase 3: Optimize (Weeks 6-8)\n"
                "Improve based on real data.\n"
                "- Conversion rate optimization\n"
                "- Messaging A/B tests\n"
                "- Scale or adjust based on U7 triggers\n"
                "- Month 2-3 planning\n\n"
                "### The Golden Rule\n"
                "**Do not skip Phase 1.** Launching a broken funnel wastes ad spend. "
                "Do not linger in Phase 1 past Week 2. Perfectionism kills momentum."
            ),
            dynamic_prompt=(
                "Design the phase overview for this client.\n\n"
                "Based on:\n"
                "- Timeline pressure: {Q41}\n"
                "- Ambition: {ambition_profile}\n"
                "- Resources: {resource_profile}\n"
                "- Triggered docs: {triggered_doc_list} (these are the assets to build)\n\n"
                "Adapt the standard 3-phase structure:\n"
                "- If {ambition_profile} = SURVIVAL: compress to 4-5 weeks total. "
                "Skip non-essential assets. Get to revenue fast.\n"
                "- If {resource_profile} = CONSTRAINED: stretch phases, lower per-week hours.\n"
                "- If {ambition_profile} = LIFESTYLE: allow more Phase 1 polish.\n\n"
                "List the specific assets (by doc ID) that belong in each phase."
            ),
        ),
        SectionSpec(
            name="Week-by-Week Plan",
            purpose="Specific tasks for each week with owners and done criteria",
            tone_note="Granular. Each week has 3-5 tasks max. Not a 50-item to-do list.",
            static_content=(
                "## Weekly Plan Structure\n\n"
                "Each week contains:\n"
                "- **3-5 tasks** (not more — focus beats volume)\n"
                "- **Owner** per task (you, team member, freelancer, automated)\n"
                "- **Time estimate** per task\n"
                "- **Done criteria**: specific, binary, testable\n"
                "  - ✅ 'Landing page is live with tracking pixel installed' — good\n"
                "  - ❌ 'Work on landing page' — bad (when is it done?)\n"
                "- **Dependencies**: what must be finished before this starts\n\n"
                "### The 80/20 Rule for Weekly Plans\n"
                "Each week, ONE task is the critical path. "
                "If that ONE task gets done, the week was successful. "
                "Mark it. Do it first."
            ),
            dynamic_prompt=(
                "Build the week-by-week plan for Weeks 1-8.\n\n"
                "Pull tasks from the triggered documents:\n"
                "- {triggered_doc_list}\n\n"
                "Map each doc to a specific week and task:\n"
                "- U3/U4/U5 → Week 1 (strategy finalization)\n"
                "- FC1/MT1 → Week 2 (asset creation)\n"
                "- Channel setup → Week 3 (go live)\n"
                "- BM docs → Week 2-3 (process setup)\n"
                "- FC4 → Week 3-4 (automation)\n"
                "- Optimization → Week 5-8\n\n"
                "Calibrate to their time: {Q45}\n"
                "- If < 5 hrs/week: max 2-3 tasks per week, stretch timeline\n"
                "- If 10-20 hrs/week: full 5-task weeks\n\n"
                "For each week, indicate:\n"
                "| Week | # | Task | Owner | Time | Done When | Depends On |\n\n"
                "Mark the ONE critical path task per week with ⭐."
            ),
        ),
        SectionSpec(
            name="Milestones & Review Checkpoints",
            purpose="Define clear milestone moments where progress is assessed",
            tone_note="Honest. 'If you're not here by Week X, something is wrong.'",
            static_content=(
                "## Milestone Checkpoints\n\n"
                "| Milestone | When | Success Criteria | If NOT Met |\n"
                "|-----------|------|-----------------|------------|\n"
                "| **M1: Foundation Complete** | End of Week 2 | All assets built, tracking live | Pause — don't launch broken |\n"
                "| **M2: First Traffic** | End of Week 3 | Channel active, first leads arriving | Troubleshoot channel setup |\n"
                "| **M3: First Client** | End of Week 5 | At least 1 new client from the system | Review offer/funnel — what's broken? |\n"
                "| **M4: Steady State** | End of Week 8 | Consistent lead flow, conversion tracking stable | Reassess channel choice |\n\n"
                "### Monthly Reviews (Post-Launch)\n"
                "- **Month 2**: Are numbers improving week-over-week? Scale or optimize.\n"
                "- **Month 3**: Hit kill-switch or scale-trigger thresholds from U7.\n"
                "- **Month 6**: Strategic review — add second channel? Raise prices? Hire?"
            ),
            dynamic_prompt=(
                "Set specific milestones for this client.\n\n"
                "Customize the standard milestones with their specific numbers:\n"
                "- M1: what 'foundation complete' means for THEIR triggered docs\n"
                "- M2: what 'first traffic' looks like for {channel}\n"
                "- M3: what 'first client' means at their deal size ({Q10})\n"
                "- M4: what 'steady state' looks like vs their target ({Q40})\n\n"
                "Add Month 2-3 optimization triggers:\n"
                "- From U7: scaling triggers, kill-switch thresholds\n"
                "- From U8: KPI thresholds that trigger optimization\n\n"
                "If {ambition_profile} = SURVIVAL: M3 deadline is Week 3, not Week 5. "
                "Everything is compressed."
            ),
        ),
        SectionSpec(
            name="Risk Mitigation",
            purpose="Anticipate what could go wrong and pre-plan responses",
            tone_note="Realistic. Not 'everything will be fine' but 'here's what to do if X happens.'",
            static_content=(
                "## Common Launch Risks\n\n"
                "| Risk | Likelihood | Impact | Mitigation |\n"
                "|------|-----------|--------|------------|\n"
                "| Channel doesn't convert | Medium | High | Test with small budget first, have backup channel |\n"
                "| Not enough time to execute | High | Medium | Reduce task count, extend timeline, outsource ONE thing |\n"
                "| Tech setup takes longer | High | Low | Use simplest tools first, upgrade later |\n"
                "| First offer doesn't resonate | Medium | High | Collect feedback fast, iterate pricing/messaging in Week 4 |\n"
                "| Analysis paralysis | High | High | Ship imperfect work. Edit live. Done > perfect. |\n\n"
                "### The #1 Risk: Not Starting\n"
                "Every week of delay is revenue not earned. "
                "The plan doesn't need to be perfect. It needs to be started."
            ),
            dynamic_prompt=(
                "Identify the top 3-5 risks specific to this client.\n\n"
                "Based on:\n"
                "- Validation flags from U1\n"
                "- Resource constraints: {Q44}, {Q45}, {Q46}\n"
                "- What hasn't worked before: {Q25}\n"
                "- Hard nos: {Q48}\n"
                "- Tech comfort: {Q47}\n\n"
                "For each risk:\n"
                "1. What could go wrong (specific to their situation)\n"
                "2. Warning signs to watch for\n"
                "3. Pre-planned response (not 'figure it out' but a specific action)\n\n"
                "If {Q25} shows a channel that failed: acknowledge it. "
                "'Google Ads didn't work before — here's what was likely wrong and what's different now.' "
                "Or: 'If it fails again, pivot to {secondary channel} by Week 6.'"
            ),
        ),
    ],
    formats=[
        FormatSpec(
            format=Format.DOC,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate the complete roadmap. "
                "The week-by-week plan as an HTML <table> for all weeks. "
                "Mark ⭐ critical path tasks with <strong>. Milestones as <h3> headings."
            ),
        ),
        FormatSpec(
            format=Format.PDF,
            method=GenerationMethod.LLM,
            model_tier=ModelTier.MAX,
            prompt_fragment=(
                "Generate a COMPLETE self-contained HTML file that will be rendered to PDF.\n"
                "Use the EXACT structure, CSS, and class names from the template below.\n"
                "Do NOT invent your own styles. Copy the CSS verbatim into a <style> tag.\n"
                "Fill in ALL bracketed placeholders with client-specific content.\n\n"
                "TEMPLATE:\n"
                "```html\n"
                '<!DOCTYPE html>\n'
                '<html lang="en">\n'
                "<head>\n"
                '<meta charset="UTF-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                "<title>Launch Roadmap</title>\n"
                "<style>\n"
                "* { margin: 0; padding: 0; box-sizing: border-box; }\n"
                'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; '
                "background: #f8f9fa; color: #1a1a1a; line-height: 1.6; padding: 20px; }\n"
                ".container { max-width: 900px; margin: 0 auto; }\n"
                "h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #1a1a1a; }\n"
                ".subtitle { color: #6c757d; font-size: 1rem; margin-bottom: 2rem; }\n"
                ".phase-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
                "color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }\n"
                ".phase-header h2 { font-size: 1.25rem; margin-bottom: 0.5rem; }\n"
                ".phase-header p { opacity: 0.9; font-size: 0.95rem; }\n"
                ".timeline { position: relative; padding: 2rem 0; }\n"
                ".timeline::before { content: ''; position: absolute; left: 50%; top: 0; bottom: 0; "
                "width: 3px; background: linear-gradient(to bottom, #3b82f6, #8b5cf6); "
                "transform: translateX(-50%); z-index:-1; }\n"
                ".week { text-align: center; margin: 2rem 0 1.5rem; position: relative; z-index: 2; }\n"
                ".week-label { display: inline-block; background: #1a1a1a; color: white; "
                "padding: 0.5rem 1.5rem; border-radius: 50px; font-weight: 600; font-size: 0.9rem; }\n"
                ".week-label.milestone { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
                "padding: 0.75rem 2rem; font-size: 1rem; }\n"
                ".task-row { display: flex; justify-content: flex-start; margin-bottom: 1rem; position: relative; }\n"
                ".task-row.right { justify-content: flex-end; }\n"
                ".task-card { background: white; border: 1px solid #e0e0e0; border-radius: 8px; "
                "padding: 1rem; width: 45%; box-shadow: 0 2px 4px rgba(0,0,0,0.05); position: relative; }\n"
                ".task-card.critical { border-left: 4px solid #667eea; }\n"
                ".task-card.critical::before { content: '⭐'; position: absolute; top: 0.5rem; "
                "right: 0.5rem; font-size: 1.2rem; }\n"
                ".task-card strong { display: block; margin-bottom: 0.5rem; color: #1a1a1a; font-size: 0.95rem; }\n"
                ".task-meta { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }\n"
                ".tag { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 50px; "
                "font-size: 0.75rem; font-weight: 500; }\n"
                ".tag-time { background: #e3f2fd; color: #1976d2; }\n"
                ".tag-doc { background: #f3e5f5; color: #7b1fa2; }\n"
                ".tag-owner { background: #e8f5e9; color: #388e3c; }\n"
                ".end-cap { text-align: center; margin: 3rem 0 2rem; position: relative; z-index: 2; }\n"
                ".end-label { display: inline-block; background: linear-gradient(135deg, #10b981, #3b82f6); "
                "color: white; padding: 0.75rem 2rem; border-radius: 25px; font-weight: 700; "
                "font-size: 1.1rem; box-shadow: 0 6px 16px rgba(16,185,129,0.3); }\n"
                ".risk-section { background: #f0f4ff; border: 1px solid #c7d2fe; border-radius: 8px; "
                "padding: 1.5rem; margin-top: 2rem; }\n"
                ".risk-section h3 { color: #4338ca; margin-bottom: 1rem; font-size: 1.1rem; }\n"
                ".risk-section ul { margin-left: 1.5rem; }\n"
                ".risk-section li { margin-bottom: 0.75rem; color: #374151; }\n"
                ".milestone-section { background: white; border: 2px solid #667eea; border-radius: 8px; "
                "padding: 1.5rem; margin-top: 2rem; }\n"
                ".milestone-section h3 { color: #667eea; margin-bottom: 1rem; font-size: 1.1rem; }\n"
                ".milestone-table { width: 100%; border-collapse: collapse; margin-top: 1rem; }\n"
                ".milestone-table th { background: #f8f9fa; padding: 0.75rem; text-align: left; "
                "font-size: 0.85rem; border-bottom: 2px solid #dee2e6; }\n"
                ".milestone-table td { padding: 0.75rem; border-bottom: 1px solid #dee2e6; font-size: 0.85rem; }\n"
                "@media (max-width: 768px) {\n"
                "  .timeline::before { left: 20px; }\n"
                "  .task-row, .task-row.right { justify-content: flex-start; padding-left: 40px; }\n"
                "  .task-card { width: 100%; }\n"
                "  h1 { font-size: 1.5rem; }\n"
                "}\n"
                "</style>\n"
                "</head>\n"
                "<body>\n"
                '<div class="container">\n\n'
                "<h1>🚀 [Title]</h1>\n"
                '<p class="subtitle">[Subtitle — timeline scope, revenue target, strategic shift]</p>\n\n'
                "<!-- Phase header: 1 per phase -->\n"
                '<div class="phase-header">\n'
                "<h2>Phase [N]: [Name] (Weeks [X]–[Y])</h2>\n"
                "<p>[Description — constraints, what gets built, what does NOT go live yet.]</p>\n"
                "</div>\n\n"
                '<div class="timeline">\n\n'
                "<!-- Week label -->\n"
                '<div class="week"><span class="week-label">Week [N] — [Theme]</span></div>\n\n'
                "<!-- Critical task (1 per week) -->\n"
                '<div class="task-row">\n'
                '<div class="task-card critical">\n'
                "<strong>[Task title]</strong>\n"
                "[Description with done criteria and concrete numbers.]\n"
                '<div class="task-meta">\n'
                '<span class="tag tag-time">[X]h</span>\n'
                '<span class="tag tag-owner">[Owner]</span>\n'
                '<span class="tag tag-doc">[DOC_ID]</span>\n'
                "</div></div></div>\n\n"
                "<!-- Secondary task (alternate .right) -->\n"
                '<div class="task-row right">\n'
                '<div class="task-card">\n'
                "<strong>[Task title]</strong>\n"
                "[Description with done criteria.]\n"
                '<div class="task-meta">\n'
                '<span class="tag tag-time">[X]h</span>\n'
                '<span class="tag tag-owner">[Owner]</span>\n'
                '<span class="tag tag-doc">[DOC_ID]</span>\n'
                "</div></div></div>\n\n"
                "<!-- Milestone label (use .milestone class) -->\n"
                '<div class="week"><span class="week-label milestone">🎯 Milestone [N]: [Name]</span></div>\n\n'
                "<!-- End cap -->\n"
                '<div class="end-cap"><span class="end-label">🚀 [Completion label]</span></div>\n\n'
                "</div>\n\n"
                "<!-- Milestone table -->\n"
                '<div class="milestone-section">\n'
                "<h3>📊 Milestones & Review Checkpoints</h3>\n"
                '<table class="milestone-table">\n'
                "<thead><tr><th>Milestone</th><th>Week</th>"
                "<th>Success Criteria</th><th>If NOT Met</th></tr></thead>\n"
                "<tbody>\n"
                "<tr><td><strong>M[N]: [Name]</strong></td><td>[When]</td>"
                "<td>[Measurable criteria]</td><td>[Action or decision]</td></tr>\n"
                "</tbody></table></div>\n\n"
                "<!-- Risk section -->\n"
                '<div class="risk-section">\n'
                "<h3>🛡️ Risk Mitigation Plan</h3>\n"
                "<ul>\n"
                "<li><strong>❓ [Risk title]</strong><br>\n"
                "Warning signs: [metric thresholds and timeline].<br>\n"
                "Response: [specific action, fallback, deadline].</li>\n"
                "</ul></div>\n\n"
                "</div>\n"
                "</body></html>\n"
                "```\n\n"
                "RULES:\n"
                "- Adapt the total number of weeks to the client (4-10 weeks). Do NOT always use 8.\n"
                "- 3 phase-header blocks. Adapt phase names and week ranges to the client's situation.\n"
                "- 1 critical .task-card per week. 1-3 secondary tasks per week.\n"
                "- Alternate .task-row and .task-row.right within each week.\n"
                "- Use .week-label.milestone for phase transitions and key checkpoints — "
                "place them where the client's plan naturally has gates, not at fixed week numbers.\n"
                "- Milestone table: 1 row per milestone + 1-2 monthly review rows.\n"
                "- Risk section: 3-5 items, each with metric-based warning signs and a concrete response.\n"
                "- Every task must have tag-time (hours) and tag-doc (source document ID). "
                "tag-owner when relevant (You, Freelancer, Team, Automated).\n"
                "- Total weekly hours per week must not exceed the client's stated availability.\n"
                "- Copy the CSS EXACTLY. Do not modify colors, spacing, or class names.\n"
                "- Output a COMPLETE self-contained HTML file. No external dependencies."
            ),
        ),
    ],
    relevant_questions=[
        "Q1", "Q4", "Q25",
        "Q40", "Q41", "Q43",
        "Q44", "Q45", "Q46", "Q47", "Q48",
    ],
    upstream_deps=[DocID.U1, DocID.U3, DocID.U4, DocID.U5, DocID.U6, DocID.U7, DocID.U8],
    downstream_consumers=[],  # U9 is the final doc — nothing depends on it
    maturity_adaptations={
        Maturity.STARTER: (
            "Stretch timeline to 8-10 weeks with lighter weekly loads. "
            "More hand-holding in task descriptions. "
            "'How to' notes alongside each task."
        ),
        Maturity.GROWING: (
            "Standard 6-8 week plan. Assume basic competence with tools. "
            "Focus on what's NEW (they already know some of this)."
        ),
        Maturity.ESTABLISHED: (
            "Compressed 4-6 week plan. They have resources. "
            "Delegate columns should include team members by role."
        ),
        Maturity.PIVOT: (
            "Parallel-track plan: build new while maintaining old revenue. "
            "Acknowledge the balancing act. Clear 'cut-over' milestone."
        ),
    },
    bottleneck_adaptations={
        Bottleneck.VISIBILITY: "Channel setup is the critical path. Prioritize Week 2-3.",
        Bottleneck.LEAD_GENERATION: "LP and lead magnet are the critical path. Prioritize Week 1-2.",
        Bottleneck.CONVERSION: "Offer and sales process are the critical path. Prioritize Week 1.",
        Bottleneck.PRICING: "Pricing restructure is Week 1, before any channel launch.",
        Bottleneck.RETENTION: "Retention system setup runs parallel to acquisition launch.",
        Bottleneck.WRONG_CLIENTS: "Positioning and avatar work are the critical path. Prioritize Week 1.",
    },
    quality_rules=[
        "Maximum 5 tasks per week. More than 5 means nothing gets done.",
        "Every task must have a binary 'done' criterion. 'Work on X' is never a task.",
        "The critical path task per week must be marked. No week has 5 equally important tasks.",
        "Time estimates must respect {Q45}. If 5 hrs/week, don't plan 20 hours of tasks.",
        "Dependencies must be explicit — don't schedule landing page ads before the landing page is built.",
        "Include buffer weeks. No plan survives contact with reality.",
        "Month 2-3 plan should be lighter (direction, not tasks) — by then they have real data.",
    ],
)