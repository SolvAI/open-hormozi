"""Shared prompt fragments injected into all document generation prompts.

These are constants — never personalized, never LLM-generated.
Kept separate so they can be updated once and propagate everywhere.
"""

from engine.models.enums import Format

# ─── Hormozi Principles ─────────────────────────────────────────

HORMOZI_PRINCIPLES = """## Core Hormozi Principles (apply to ALL outputs)

1. **Value Equation**: Value = (Dream Outcome × Likelihood) / (Time × Effort). Always optimize all 4.
2. **Grand Slam Offer**: Make the offer so good people feel stupid saying no.
3. **Starving Crowd**: The market matters more than the offer. Find desperate buyers first.
4. **One Channel Mastery**: Under $1M, pick ONE acquisition channel and master it.
5. **Price-to-Value Gap**: Charge based on value delivered, never on time spent or cost-plus.
6. **Lead Magnets as Filters**: Free content should qualify leads, not just attract eyeballs.
7. **Volume × Quality × Conversion**: Fix the weakest link first.
8. **Never Discount — Add Bonuses**: Discounting destroys perceived value. Stack value instead.
9. **Proof Over Promise**: One case study beats 100 claims. Build proof into every stage.
10. **Speed to First Value**: The faster a client gets a result, the more they trust and buy again.
"""

# ─── Quality Baseline ───────────────────────────────────────────

QUALITY_BASELINE = """## Output Quality Rules

**LENGTH: Your output must be 100-500 words. NEVER exceed 1000 words. Be ruthlessly concise.**

- Write ONLY personalized recommendations specific to THIS client. No generic theory, no frameworks, no educational preamble.
- Every sentence must reference the client's specific situation, numbers, or answers.
- If a sentence could apply to any business, DELETE IT.
- Use the client's own vocabulary (from their form answers) when writing about their business.
- Numbers over adjectives: "increase from $4k to $10k/mo" not "significantly grow revenue."
- Bullet points and tables over paragraphs. Scannable over readable.
- Every recommendation: WHO does WHAT by WHEN with WHAT TOOL. No vague advice.
- Match tone to maturity: STARTER = encouraging + concrete. ESTABLISHED = direct + strategic.
- **FORMAT REMINDER: These instructions use markdown for readability, but your OUTPUT must follow the format specified below (e.g., HTML tags for DOC format). Never output markdown syntax (##, **, ```) in your response.**
"""

# ─── Format Instructions ────────────────────────────────────────

FORMAT_INSTRUCTIONS: dict[Format, str] = {
    Format.DOC: (
        "Output as an HTML fragment (no <html>, <head>, or <body> — just the content).\n"
        "It will be wrapped in a branded template with professional CSS.\n"
        "Write 100-500 words. NEVER exceed 800.\n"
        "\n"
        "Use these HTML elements — they are all styled by the brand CSS:\n"
        "\n"
        "STRUCTURE:\n"
        "  <h2>Major Section</h2>           — bordered bottom, large\n"
        "  <h3>Subsection</h3>              — medium weight\n"
        "  <h4>Sub-subsection</h4>          — small, muted color\n"
        "  <p>Paragraph text</p>            — standard body copy\n"
        "  <hr>                             — section divider\n"
        "\n"
        "INLINE:\n"
        "  <strong>bold</strong>  <em>italic</em>  <u>underline</u>\n"
        "  <mark>highlighted text</mark>    — yellow background\n"
        "  <code>inline code</code>         — monospace with background\n"
        "  <a href=\"#\">link text</a>\n"
        "\n"
        "LISTS:\n"
        "  <ul><li>Bullet item</li></ul>    — custom dot bullets\n"
        "  <ol><li>Numbered item</li></ol>  — decimal numbers\n"
        "  Nest freely: <li>Parent<ul><li>Child</li></ul></li>\n"
        "\n"
        "TABLE:\n"
        "  <table><thead><tr><th>Header</th></tr></thead>\n"
        "         <tbody><tr><td>Cell</td></tr></tbody></table>\n"
        "\n"
        "BLOCKQUOTE:\n"
        "  <blockquote><p>Quote text — attribution</p></blockquote>\n"
        "\n"
        "CODE BLOCK:\n"
        "  <pre><code>multi-line code here</code></pre>\n"
        "\n"
        "DEFINITION LIST:\n"
        "  <dl><dt>Term</dt><dd>Definition text</dd></dl>\n"
        "\n"
        "CALLOUT (tip):\n"
        "  <div class=\"callout\">\n"
        "    <div class=\"callout-icon\">💡</div>\n"
        "    <div><p><strong>Tip:</strong> advice here</p></div>\n"
        "  </div>\n"
        "\n"
        "CALLOUT (warning):\n"
        "  <div class=\"callout callout-warn\">\n"
        "    <div class=\"callout-icon\">⚠️</div>\n"
        "    <div><p><strong>Warning:</strong> caution here</p></div>\n"
        "  </div>\n"
        "\n"
        "METRIC CARDS (row of 2-4 numbers):\n"
        "  <div class=\"metric-row\">\n"
        "    <div class=\"metric\">\n"
        "      <div class=\"metric-value\">$2,500</div>\n"
        "      <div class=\"metric-label\">Avg Deal Size</div>\n"
        "    </div>\n"
        "    <!-- repeat for each metric -->\n"
        "  </div>\n"
        "\n"
        "BADGE (inline tag):\n"
        "  <span class=\"badge\">Included</span>\n"
        "\n"
        "IMAGE PLACEHOLDER:\n"
        "  <div class=\"img-placeholder\">📊 Description of visual asset</div>\n"
        "\n"
        "SECTION LEAD-IN (optional, one per <h2>, sets up the section in one line):\n"
        "  <p class=\"lead\">One sentence that sets up what this section decides.</p>\n"
        "\n"
        "STEP LIST (numbered actions with emphasis on the number):\n"
        "  <ol class=\"steps\"><li><strong>Action</strong>: concrete detail.</li></ol>\n"
        "\n"
        "KEY TAKEAWAY (closes a section, max one per <h2>):\n"
        "  <p class=\"takeaway\">Key takeaway: the one sentence that matters.</p>\n"
        "\n"
        "RULES:\n"
        "- Do NOT include <html>, <head>, <body>, <style>, or <script> tags.\n"
        "- Do NOT wrap output in ```html fences.\n"
        "- Output ONLY the content that goes inside <div class=\"page\">.\n"
        "- Every sentence must reference THIS client's specific data.\n"
        "- Use metric cards for 2-4 key numbers. Use tables for comparisons.\n"
        "- Use callouts sparingly (max 2 per document).\n"
        "- Amounts as `$2,500`. No em dashes: use a colon, comma or parentheses.\n"
    ),
    Format.XLS: (
        "Output as JSON representing an Excel structure:\n"
        "```json\n"
        '{"sheets": [{"name": "Sheet Name", "headers": ["Col A", "Col B"], '
        '"rows": [["val1", "val2"]], '
        '"formulas": {"C2": "=A2*B2"}, '
        '"formatting": {"A1:Z1": "bold_header"}}]}\n'
        "```\n"
        "Prefill cells with client data where available.\n"
        "Mark user-input cells with [USER INPUT].\n"
        "Include Excel formulas in Excel notation (=SUM, =IF, =VLOOKUP).\n"
        "Keep to 2 sheets max. Concise headers."
    ),
    Format.HTML: (
        "Output a single self-contained HTML file with inline CSS.\n"
        "Responsive, mobile-first. Clean semantic HTML5.\n"
        "All text content filled with client-specific copy — no placeholders.\n"
        "The HTML must be deployable as-is."
    ),
    Format.MERMAID: (
        "Output a valid Mermaid diagram.\n"
        "Use the appropriate type (flowchart TD, gantt, sequenceDiagram, etc.).\n"
        "Every node must have a clear, jargon-free label.\n"
        "Wrap labels in quotes if they contain special characters.\n"
        "Do NOT use parentheses or brackets inside node labels without quoting.\n"
        "Include notes on decision branches where relevant.\n"
        "Maximum 20 nodes for readability."
    ),
    Format.PNG: (
        "Output an HTML+CSS snippet designed to be screenshotted at 1200×800px.\n"
        "Use fixed dimensions, no scrolling.\n"
        "Clean, modern, printable design.\n"
        "ALL text content must be filled — this is a final client deliverable."
    ),
    Format.PDF: (
        "Output HTML+CSS formatted for A4 print (210mm × 297mm).\n"
        "Include page-break-before hints for major sections.\n"
        "Clean typography, professional layout.\n"
        "Will be rendered to PDF — no JavaScript dependencies."
    ),
    Format.CHART: (
        "Output JSON data for Chart.js:\n"
        "```json\n"
        '{"type": "line", "data": {"labels": [...], '
        '"datasets": [{"label": "...", "data": [...]}]}, '
        '"options": {"scales": {...}}}\n'
        "```\n"
        "Include axis labels, legend text, and chart title."
    ),
    Format.SLIDES: (
        "Output structured JSON for a slide deck:\n"
        "```json\n"
        '[{"slide": 1, "title": "...", "bullets": ["...", "..."], '
        '"speaker_notes": "Full script for this slide..."}]\n'
        "```\n"
        "Max 3 bullets per slide. Speaker notes contain the complete talk track."
    ),
}