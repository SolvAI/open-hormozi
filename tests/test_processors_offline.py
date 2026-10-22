"""Test all processors with synthetic content — no LLM calls.

Feeds pre-built content directly to each processor to verify rendering,
file creation, and format correctness.

Usage:
    python -m tests.test_processors_lorem                     # all specs, all formats
    python -m tests.test_processors_lorem --doc U3            # one spec
    python -m tests.test_processors_lorem --format doc        # one format across all specs
    python -m tests.test_processors_lorem --output-dir ./tmp  # custom output
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from engine.models.enums import DocID, Format, GenerationMethod
from engine.models.registry import DocSpec, FormatSpec
from engine.processors.registry import get_processor, PROCESSORS
from engine.specs import ALL_SPECS

logger = logging.getLogger(__name__)


# ═════════════════════════════════════════════════════════════════
#  SAMPLE CONTENT — HTML (for Format.DOC, now branded PDF)
# ═════════════════════════════════════════════════════════════════

SAMPLE_DOC_HTML = """\
<h2>Value Equation Diagnostic</h2>
<p>Your current offer scores across the four dimensions of Hormozi's Value Equation.
Each dimension is rated <strong>1–10</strong> based on your intake answers.</p>

<div class="metric-row">
  <div class="metric">
    <div class="metric-value">8/10</div>
    <div class="metric-label">Dream Outcome</div>
  </div>
  <div class="metric">
    <div class="metric-value">5/10</div>
    <div class="metric-label">Perceived Likelihood</div>
  </div>
  <div class="metric">
    <div class="metric-value">6/10</div>
    <div class="metric-label">Time to Result</div>
  </div>
  <div class="metric">
    <div class="metric-value">7/10</div>
    <div class="metric-label">Effort &amp; Sacrifice</div>
  </div>
</div>

<p>The primary gap is <strong>Perceived Likelihood</strong> — your audience isn't
confident it will work <em>for them specifically</em>. This is a
<mark>proof problem</mark>, not an offer problem.</p>

<h2>Value Stack Design</h2>
<p>Your restructured offer packages each component with named value and anchored price.</p>

<table>
  <thead>
    <tr><th>Component</th><th>Deliverable</th><th>Anchored Value</th><th>Status</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Core</strong></td>
      <td>Full strategy build-out with 90-day implementation plan</td>
      <td>$4,500</td>
      <td><span class="badge">Included</span></td>
    </tr>
    <tr>
      <td><strong>Bonus 1</strong></td>
      <td>CTO Quick-Win Audit — first deliverable in 48h</td>
      <td>$800</td>
      <td><span class="badge">Included</span></td>
    </tr>
    <tr>
      <td><strong>Bonus 2</strong></td>
      <td>Monthly strategy call for 3 months</td>
      <td>$1,200</td>
      <td><span class="badge">Included</span></td>
    </tr>
  </tbody>
</table>

<p>Total anchored value: <strong>$6,500</strong>. Asking price: <strong>$2,500</strong>.
Price-to-value ratio: <strong>2.6×</strong>.</p>

<h2>Guarantee Design</h2>

<h3>Recommended: Conditional Guarantee</h3>
<p>Based on your <u>moderate proof level</u> and $2,500 deal size:</p>

<ol>
  <li>Complete all 3 implementation sprints</li>
  <li>If no measurable pipeline improvement by day 90</li>
  <li>Full strategy rebuild at no cost</li>
</ol>

<div class="callout">
  <div class="callout-icon">💡</div>
  <div><p><strong>Implementation tip:</strong> State the guarantee on your landing page
  AND in your proposal. Saying it twice doubles persuasive impact.</p></div>
</div>

<h3>Scarcity Mechanism</h3>
<ul>
  <li>Capacity limit: maximum <strong>4 new clients/month</strong> (real — solo operator)</li>
  <li>Bonus window: Quick-Win Audit only for contracts signed within 7 days</li>
  <li>No fake countdown timers — ever</li>
</ul>

<div class="callout callout-warn">
  <div class="callout-icon">⚠️</div>
  <div><p><strong>Validation flag:</strong> Deal size ($2,500) × volume (4/mo) = $10,000/mo.
  That requires <u>100% close rate</u>. Realistically you need 8–10 qualified leads/month.</p></div>
</div>

<h2>Ascension Model</h2>

<blockquote>
  <p>"The goal isn't to sell everyone the most expensive thing. It's to give everyone
  the right next step." — Alex Hormozi</p>
</blockquote>

<h4>Tier Architecture</h4>
<dl>
  <dt>Entry — Strategy Sprint ($800)</dt>
  <dd>2-week engagement. One deliverable: a prioritized action plan.</dd>

  <dt>Core — Full Strategy Build ($2,500)</dt>
  <dd>The Grand Slam Offer above. 90-day plan with all bonuses. 60–70% of revenue.</dd>

  <dt>Premium — Ongoing Advisory ($1,500/mo)</dt>
  <dd>Monthly retainer. Strategy calls, KPI review, quarterly recalibration.</dd>
</dl>

<hr>

<h3>Naming Convention</h3>
<p>Apply the <code>MAGIC</code> framework:</p>

<pre><code>M — Magnet word:    "Accelerator"
A — Avatar:         "for B2B consultants"
G — Goal:           "to fill your pipeline"
I — Interval:       "in 90 days"
C — Container:      "system"

→ "The Pipeline Accelerator"</code></pre>

<h3>Next Steps</h3>
<ul>
  <li><a href="#">U4 — Pricing &amp; Packaging</a> → tier pricing math</li>
  <li><a href="#">U5 — Positioning &amp; Messaging</a> → how to communicate this</li>
  <li><a href="#">FC1 — Landing Page</a> → convert this offer to a page</li>
</ul>

<div class="img-placeholder">
  📊 Value Stack Visualization — generated as a separate PNG asset
</div>
"""


# ═════════════════════════════════════════════════════════════════
#  SAMPLE CONTENT — OTHER FORMATS
# ═════════════════════════════════════════════════════════════════

SAMPLE_MERMAID_FLOWCHART = """\
flowchart TD
    A["Website Visit"] --> B{"Qualified?"}
    B -->|"Yes"| C["Book Discovery Call"]
    B -->|"No"| D["Lead Magnet Download"]
    C --> E{"Show Up?"}
    E -->|"Yes"| F["Discovery Call"]
    E -->|"No"| G["No-Show Recovery Email"]
    F --> H{"Close?"}
    H -->|"Yes"| I["Onboarding"]
    H -->|"No"| J["Follow-Up Sequence"]
    D --> K["Nurture Email Sequence"]
    G --> C
    J --> K
    K --> B
"""

SAMPLE_MERMAID_GANTT = """\
gantt
    title Launch Roadmap
    dateFormat YYYY-MM-DD
    section Phase 1: Foundation
    Finalize offer (U3/U4)     :a1, 2025-07-01, 5d
    Build landing page (FC1)   :a2, after a1, 5d
    Set up tracking (U8)       :a3, after a1, 3d
    section Phase 2: Launch
    Activate channel           :b1, after a2, 3d
    First leads                :b2, after b1, 7d
    section Phase 3: Optimize
    Conversion optimization    :c1, after b2, 14d
    Scale decision             :milestone, after c1, 0d
"""


def _sample_xls_inject() -> dict:
    """JSON with row_injections — matches template-inject mode."""
    return {
        "row_injections": [
            {
                "sheet": "Sheet1",
                "start_row": 2,
                "rows": [
                    ["Keyword Alpha", "Exact", "Ad Group 1", "Campaign 1",
                     "High", 2.50, 320, "Medium", "High", "To launch", ""],
                    ["Keyword Beta", "Phrase", "Ad Group 1", "Campaign 1",
                     "Pain-aware", 1.80, 540, "Low", "Medium", "To launch", ""],
                    ["Keyword Gamma", "Broad", "Ad Group 2", "Campaign 2",
                     "Competitor", 3.10, 210, "High", "High", "To launch", ""],
                ],
            }
        ]
    }


def _sample_xls_scratch() -> dict:
    """JSON for from-scratch XLS creation (no template)."""
    return {
        "sheets": [
            {
                "name": "Pricing Tiers",
                "headers": ["Tier", "Description", "Price", "Anchor Value", "Margin %"],
                "rows": [
                    ["Sprint", "2-week strategy sprint", 800, 1500, "65%"],
                    ["Core", "Full 90-day build-out", 2500, 7100, "72%"],
                    ["Premium", "Ongoing monthly advisory", 1500, 3000, "80%"],
                ],
            },
            {
                "name": "Revenue Scenarios",
                "headers": ["Scenario", "Clients/Mo", "Avg Deal", "Monthly Rev", "Annual Rev"],
                "rows": [
                    ["Conservative", 2, 2500, 5000, 60000],
                    ["Realistic", 3, 2800, 8400, 100800],
                    ["Optimistic", 4, 3200, 12800, 153600],
                ],
            },
        ]
    }


def _sample_png_json(doc_id: str, template_path: str | None) -> dict:
    """JSON matching common PNG template schemas."""
    schemas: dict[str, dict] = {
        "u2_persona_card": {
            "persona_name": "Marc",
            "persona_title": "CTO of SaaS startup, 35 yrs",
            "key_quote": "I need a senior dev yesterday — my CTO just quit.",
            "demographics": ["Age: 30–45", "Location: Paris", "Company: 10–50 emp"],
            "top_pains": [
                "Can't find reliable senior talent",
                "Previous freelancers disappeared mid-project",
                "Release deadline in 6 weeks",
            ],
            "desired_outcomes": [
                "Working MVP delivered on time",
                "Codebase I can hand to a future CTO",
                "Sleep through the night again",
            ],
            "buying_triggers": ["CTO quit", "Funding round closing"],
            "channels": ["LinkedIn", "Tech Slack communities"],
        },
        "bm4_staff_cheat_sheet": {
            "business_name": "Acme Bistro",
            "sections": [
                {"title": "Greeting",
                 "script": "Welcome! Table for how many today?",
                 "if_no": "No worries, have a great day!"},
                {"title": "Upsell: Dessert",
                 "script": "Our chef's special today is the tarte tatin.",
                 "if_no": "No problem — can I get you a coffee instead?"},
                {"title": "Complaint",
                 "steps": ["1. Apologize sincerely", "2. Fix immediately", "3. Small bonus"]},
                {"title": "Farewell",
                 "script": "Thank you! We'd love to see you again."},
            ],
        },
        "bm5_loyalty_card": {
            "card_type": "loyalty",
            "headline": "Acme Rewards",
            "subline": "Collect stamps, earn free sessions",
            "reward": "10th session FREE",
            "terms": "One stamp per visit. Non-transferable.",
            "brand_name": "Acme Consulting",
        },
        "u5_positioning_map": {
            "axis_x": {"label": "Price", "low": "Budget", "high": "Premium"},
            "axis_y": {"label": "Service Level", "low": "DIY", "high": "Done-for-you"},
            "positions": [
                {"name": "You", "x": 0.75, "y": 0.8, "highlight": True},
                {"name": "Upwork Average", "x": 0.2, "y": 0.3, "highlight": False},
                {"name": "Big Agency", "x": 0.9, "y": 0.9, "highlight": False},
                {"name": "DIY Tools", "x": 0.1, "y": 0.1, "highlight": False},
            ],
        },
        "mt1_case_study_card": {
            "cards": [
                {"client_name": "TechStartup.io", "industry": "SaaS",
                 "challenge": "No pipeline, burning runway",
                 "result": "22 qualified leads in 6 weeks, $180k pipeline",
                 "quote": "Thomas turned our panic into a system.",
                 "quote_author": "Marie Dupont, CEO"},
            ],
        },
    }
    if template_path:
        for key, schema in schemas.items():
            if key in template_path:
                return schema

    # Fallback: generic data
    return {
        "title": f"{doc_id} Visual",
        "headline": "Sample Headline",
        "items": ["Item one", "Item two", "Item three"],
        "footer": "Generated by Hormozi System",
    }


def _sample_chart_json() -> dict:
    return {
        "type": "line",
        "data": {
            "labels": ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"],
            "datasets": [
                {"label": "Conservative",
                 "data": [4200, 5100, 6400, 7500, 8200, 9000],
                 "borderColor": "#2563eb", "tension": 0.3},
                {"label": "Optimistic",
                 "data": [4200, 6000, 8000, 10000, 11500, 13000],
                 "borderColor": "#16a34a", "borderDash": [5, 5], "tension": 0.3},
            ],
        },
        "options": {
            "plugins": {"title": {"display": True, "text": "6-Month Revenue Projection"}},
            "scales": {"y": {"beginAtZero": False,
                             "title": {"display": True, "text": "Revenue ($)"}}},
        },
    }


def _sample_standalone_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">
<style>
  body { font-family: Inter, sans-serif; margin: 0; padding: 32px; color: #1d1d1f; }
  .hero { background: #2563eb; color: white; padding: 48px 32px; border-radius: 12px;
          margin-bottom: 24px; }
  .hero h1 { margin: 0 0 8px; font-size: 28px; }
  .hero p { margin: 0; opacity: .85; }
  h2 { font-size: 20px; border-bottom: 2px solid #dbeafe; padding-bottom: 8px; }
  ul { padding-left: 20px; }
  li { margin-bottom: 6px; }
  .cta { display: inline-block; background: #2563eb; color: white; padding: 12px 28px;
         border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 16px; }
</style>
</head>
<body>
<div class="hero">
  <h1>Book Your Free Strategy Session</h1>
  <p>In 20 minutes, we'll map your 90-day growth plan.</p>
</div>
<div>
  <h2>What You'll Get</h2>
  <ul>
    <li><strong>Personalized growth audit</strong></li>
    <li><strong>Top 3 quick wins</strong> — actionable within 7 days</li>
    <li><strong>90-day roadmap</strong></li>
  </ul>
  <a href="#" class="cta">Book My Session →</a>
</div>
</body>
</html>"""


def _sample_slides_json() -> str:
    return json.dumps([
        {"slide": 1, "section": "Hook",
         "title": "What If You Could 3× Your Pipeline in 90 Days?",
         "bullets": ["No cold calling", "No paid ads", "Just a better offer"],
         "speaker_notes": "Open with the big promise. Pause for effect."},
        {"slide": 2, "section": "Problem",
         "title": "The Real Reason Clients Don't Buy",
         "bullets": ["It's not your skill", "It's not your price", "It's your OFFER"],
         "speaker_notes": "Agitate the pain. Reference common frustrations."},
    ])


# ═════════════════════════════════════════════════════════════════
#  CONTENT ROUTER
# ═════════════════════════════════════════════════════════════════

def get_sample_content(doc_id: DocID, format_spec: FormatSpec) -> Any:
    """Return synthetic content appropriate for a (doc, format) pair."""
    fmt = format_spec.format

    if fmt == Format.DOC:
        return SAMPLE_DOC_HTML

    if fmt == Format.MERMAID:
        return SAMPLE_MERMAID_GANTT if doc_id == DocID.U9 else SAMPLE_MERMAID_FLOWCHART

    if fmt == Format.XLS:
        if format_spec.template_path and Path(format_spec.template_path).exists():
            return _sample_xls_for_template(doc_id, format_spec.template_path)
        return _sample_xls_scratch()

    if fmt == Format.PNG:
        return _sample_png_json(doc_id.value, format_spec.template_path)

    if fmt in (Format.HTML, Format.PDF):
        return _sample_standalone_html()

    if fmt == Format.CHART:
        return _sample_chart_json()

    if fmt == Format.SLIDES:
        return _sample_slides_json()

    raise ValueError(f"No sample for format: {fmt.value}")

def _sample_xls_for_template(doc_id: DocID, template_path: str) -> dict:
    """Build XLS inject data whose sheet names match the actual template."""
    from openpyxl import load_workbook

    wb = load_workbook(template_path, read_only=True)
    sheet_names = wb.sheetnames
    wb.close()

    # Per-doc sample rows keyed by sheet name
    _SAMPLES: dict[str, dict[str, list[list]]] = {
        "CH1": {
            "Keyword Master List": [
                ["react developer freelance", "Exact", "High Intent", "Search - High Intent",
                 "High", 3.20, 480, "Medium", "High", "To launch", ""],
                ["hire senior developer", "Phrase", "High Intent", "Search - High Intent",
                 "High", 2.80, 320, "Medium", "High", "To launch", ""],
                ["CTO as a service", "Exact", "Pain-Aware", "Search - Pain",
                 "Pain-aware", 4.10, 110, "Low", "Medium", "To launch", ""],
            ],
            "Negative Keywords": [
                ["free", "Phrase", "All", "Excludes freebie seekers"],
                ["tutorial", "Phrase", "All", "Excludes learners"],
                ["salary", "Exact", "All", "Excludes job seekers"],
                ["internship", "Phrase", "All", "Excludes students"],
            ],
            "Ad Groups Structure": [
                ["Search - High Intent", "Hire Developer", "High-intent hiring keywords",
                 3, "Hire Senior React Dev", "Ship Your MVP in 6 Weeks",
                 "Expert freelance developers for startups. 6-week MVP delivery guaranteed."],
                ["Search - Pain", "CTO Problems", "Pain-aware CTO searches",
                 2, "Your CTO Just Quit?", "Emergency Dev Leadership",
                 "Senior dev expertise on demand. First deliverable in 48 hours."],
            ],
        },
        "U4": {
            "Pricing Tiers": [
                ["Strategy Sprint", "2-week focused engagement", 800, 1500,
                 None, 200, None, None, "No"],
                ["Full Strategy Build", "90-day implementation plan", 2500, 7100,
                 None, 600, None, None, "Yes"],
                ["Ongoing Advisory", "Monthly retainer", 1500, 3000,
                 None, 300, None, None, "No"],
            ],
            "LTV Calculator": [
                [None, 2500],
                [None, 3],
                [None, 1.5],
                [None, None],
                [None, None],
                [None, 800],
            ],
            "Break-Even": [
                [None, 2200],
                [None, 2500],
                [None, 600],
            ],
        },
    }

    doc_key = doc_id.value
    doc_samples = _SAMPLES.get(doc_key, {})

    injections = []
    for sheet_name in sheet_names:
        rows = doc_samples.get(sheet_name)
        if rows:
            injections.append({
                "sheet": sheet_name,
                "start_row": 2,
                "rows": rows,
            })
        # If no sample rows for this sheet, skip it (leave template as-is)

    if not injections:
        # Fallback: inject generic data into the first sheet
        injections.append({
            "sheet": sheet_names[0],
            "start_row": 2,
            "rows": [
                ["Sample A", "Value 1", 100, 200],
                ["Sample B", "Value 2", 300, 400],
            ],
        })

    return {"row_injections": injections}

# ═════════════════════════════════════════════════════════════════
#  TEST RUNNER
# ═════════════════════════════════════════════════════════════════

def run_test(
    specs: dict[DocID, DocSpec],
    format_filter: str | None,
    output_dir: Path,
) -> dict:
    """Process all (spec, format) pairs. Returns results summary."""

    results: list[dict] = []
    passed = failed = skipped = 0

    for doc_id, spec in sorted(specs.items(), key=lambda kv: kv[0].value):
        for format_spec in spec.formats:

            tag = f"{doc_id.value}.{format_spec.format.value}"

            # Skip static assets
            if format_spec.method == GenerationMethod.STATIC:
                skipped += 1
                results.append({"doc": doc_id.value, "format": format_spec.format.value,
                                "status": "SKIP", "reason": "static asset"})
                continue

            # Format filter
            if format_filter and format_spec.format.value != format_filter:
                continue

            # Processor available?
            try:
                processor = get_processor(format_spec.format)
            except KeyError:
                skipped += 1
                results.append({"doc": doc_id.value, "format": format_spec.format.value,
                                "status": "SKIP", "reason": "no processor"})
                continue

            # Sample content
            try:
                content = get_sample_content(doc_id, format_spec)
            except Exception as e:
                skipped += 1
                results.append({"doc": doc_id.value, "format": format_spec.format.value,
                                "status": "SKIP", "reason": f"no sample: {e}"})
                continue

            # Process
            doc_dir = output_dir / doc_id.value
            start = time.time()
            try:
                file_path = processor.process(
                    content=content,
                    doc_id=doc_id.value,
                    output_dir=doc_dir,
                    template_path=format_spec.template_path,
                    metadata={"doc_name": spec.name, "format": format_spec.format.value},
                )
                elapsed = time.time() - start
                exists = file_path.exists()
                size = file_path.stat().st_size if exists else 0

                if exists and size > 0:
                    passed += 1
                    status = "PASS"
                else:
                    failed += 1
                    status = "FAIL"

                results.append({
                    "doc": doc_id.value, "format": format_spec.format.value,
                    "status": status,
                    "file": str(file_path.relative_to(output_dir)),
                    "size_kb": round(size / 1024, 1),
                    "time_s": round(elapsed, 2),
                    "ext": file_path.suffix,
                })

            except Exception as e:
                elapsed = time.time() - start
                failed += 1
                results.append({
                    "doc": doc_id.value, "format": format_spec.format.value,
                    "status": "ERROR", "error": str(e)[:200],
                    "time_s": round(elapsed, 2),
                })

    return {"results": results, "passed": passed, "failed": failed, "skipped": skipped}


# ═════════════════════════════════════════════════════════════════
#  REPORT
# ═════════════════════════════════════════════════════════════════

def print_report(summary: dict, output_dir: Path) -> None:
    p, f, s = summary["passed"], summary["failed"], summary["skipped"]
    total = p + f + s

    print("\n" + "═" * 74)
    print(f"  PROCESSOR TEST — {total} pairs  ({p} pass · {f} fail · {s} skip)")
    print("═" * 74)

    for r in summary["results"]:
        icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭️ "}.get(r["status"], "?")
        line = f"  {icon} {r['doc']:5s} .{r['format']:8s}"

        if r["status"] == "PASS":
            line += f"  → {r['ext']:5s} {r['size_kb']:8.1f} KB  ({r['time_s']:.2f}s)"
        elif r["status"] in ("FAIL", "ERROR"):
            line += f"  → {r.get('error', 'empty file')}"
        else:
            line += f"  → {r.get('reason', '')}"
        print(line)

    print("─" * 74)
    print(f"  Output: {output_dir}")
    if f > 0:
        print(f"  ⚠️  {f} failure(s)")
    else:
        print("  🎉 All processors OK")
    print("═" * 74 + "\n")


# ═════════════════════════════════════════════════════════════════
#  CLI
# ═════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(description="Test processors with synthetic content")
    parser.add_argument("--doc", type=str, default=None, help="Single doc, e.g. U3")
    parser.add_argument("--format", type=str, default=None, help="Single format, e.g. doc")
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--keep", action="store_true", help="Don't clean output dir")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)-8s %(name)s: %(message)s",
    )

    out = Path(args.output_dir) if args.output_dir else Path("/tmp/hormozi_test_processors")
    if out.exists() and not args.keep:
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    if args.doc:
        try:
            target = DocID(args.doc.upper())
        except ValueError:
            print(f"Unknown doc: {args.doc}. Available: {[d.value for d in DocID]}")
            return 1
        specs = {target: ALL_SPECS[target]}
    else:
        specs = ALL_SPECS

    print(f"\nProcessors: {[f.value for f in PROCESSORS]}")
    print(f"Specs: {len(specs)}, format filter: {args.format or 'all'}\n")

    summary = run_test(specs, args.format, out)
    print_report(summary, out)
    return 1 if summary["failed"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())