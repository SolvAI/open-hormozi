"""Mermaid syntax validation and common auto-fixes.

Does NOT render — just ensures the diagram text is valid before saving.
Rendering to PNG uses headless Chromium (Playwright) with mermaid.js.
"""

from __future__ import annotations

import re
import logging
import json
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# mermaid.js CDN (pinned version for reproducibility)
_MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

_MERMAID_BLOCK = re.compile(
    r"```mermaid\s*\n(.*?)```",
    re.DOTALL,
)


def extract_diagram(text: str) -> str:
    """Extract a Mermaid diagram from a larger response.

    Tries in order:
      1. Find a ```mermaid ... ``` fenced code block
      2. Find the first line starting with a known diagram type and take everything from there
      3. Return the original text as-is (fallback)
    """
    # 1. Fenced code block
    match = _MERMAID_BLOCK.search(text)
    if match:
        return match.group(1).strip()

    # 2. Find first line with a known diagram type
    lines = text.split("\n")
    start_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if _TYPE_PATTERN.match(stripped):
            start_idx = i
            break

    if start_idx is not None:
        # Take from the diagram type line to the end (or next ``` fence)
        diagram_lines = []
        for line in lines[start_idx:]:
            if line.strip() == "```":
                break
            diagram_lines.append(line)
        extracted = "\n".join(diagram_lines).strip()
        if len(extracted) > 20:  # sanity check — not just the type keyword
            return extracted

    # 3. Fallback: return as-is
    return text

# ─── Common LLM mistakes in Mermaid output ──────────────────────

_FIXES: list[tuple[re.Pattern, str, str]] = [
    # Remove markdown code fences wrapping the diagram
    (re.compile(r"^```mermaid\s*\n", re.MULTILINE), "", "strip opening fence"),
    (re.compile(r"^```\s*$", re.MULTILINE), "", "strip closing fence"),
    # Fix unquoted labels with special chars  (A[some (thing)] → A["some (thing)"])
    (
        re.compile(r'(\w+)\[([^\]"]*[()&][^\]"]*)\]'),
        r'\1["\2"]',
        "quote labels with parens/ampersands",
    ),
    # Fix unquoted labels in round brackets
    (
        re.compile(r'(\w+)\(([^)"]*[&<>][^)"]*)\)'),
        r'\1("\2")',
        "quote labels with special chars in round brackets",
    ),
    # Remove empty lines inside diagram (can break some parsers)
    (re.compile(r"\n{3,}"), "\n\n", "collapse triple+ newlines"),
    # Fix common LLM artifact: "---" as a separator inside diagrams
    (re.compile(r"^---+\s*$", re.MULTILINE), "", "remove horizontal rules"),
]

# ─── Diagram type detection ─────────────────────────────────────

_DIAGRAM_TYPES = [
    "graph", "flowchart", "sequenceDiagram", "classDiagram",
    "stateDiagram", "erDiagram", "gantt", "pie", "gitgraph",
    "mindmap", "timeline", "sankey", "xychart",
]

_TYPE_PATTERN = re.compile(
    r"^\s*(" + "|".join(_DIAGRAM_TYPES) + r")\b",
    re.MULTILINE | re.IGNORECASE,
)


def detect_diagram_type(mermaid_text: str) -> Optional[str]:
    """Detect the Mermaid diagram type from source text."""
    match = _TYPE_PATTERN.search(mermaid_text)
    if match:
        return match.group(1).strip()
    return None


def validate_and_fix(mermaid_text: str) -> tuple[str, list[str]]:
    """Apply extraction, auto-fixes, and basic validation.

    Returns:
        (fixed_text, list_of_fixes_applied)
    """
    applied: list[str] = []

    # Step 0: Extract diagram if embedded in larger content
    extracted = extract_diagram(mermaid_text)
    if extracted != mermaid_text:
        applied.append("extracted diagram from mixed content")
    fixed = extracted.strip()

    for pattern, replacement, description in _FIXES:
        if pattern.search(fixed):
            fixed = pattern.sub(replacement, fixed)
            applied.append(description)

    fixed = fixed.strip()

    # Validate: must start with a known diagram type
    diagram_type = detect_diagram_type(fixed)
    if not diagram_type:
        logger.warning(
            "Mermaid diagram doesn't start with a known type. "
            f"First 80 chars: {fixed[:80]!r}"
        )

    # Validate: balanced brackets/quotes
    issues = _check_balance(fixed)
    if issues:
        for issue in issues:
            logger.warning(f"Mermaid balance issue: {issue}")

    return fixed, applied


def _check_balance(text: str) -> list[str]:
    """Check for unbalanced brackets and quotes."""
    issues = []
    pairs = {"[": "]", "(": ")", "{": "}"}
    stack: list[str] = []

    in_string = False
    quote_char = ""

    for i, ch in enumerate(text):
        if ch in ('"', "'") and not in_string:
            in_string = True
            quote_char = ch
        elif ch == quote_char and in_string:
            in_string = False
            quote_char = ""
        elif not in_string:
            if ch in pairs:
                stack.append(ch)
            elif ch in pairs.values():
                expected_open = [k for k, v in pairs.items() if v == ch]
                if stack and stack[-1] in expected_open:
                    stack.pop()
                elif not stack:
                    issues.append(f"Unmatched closing '{ch}' at position {i}")

    if stack:
        issues.append(f"Unclosed brackets: {''.join(stack)}")

    return issues


def render_to_png(
    mermaid_text: str,
    output_path: Path,
    width: int = 1200,
    theme: str = "default",
) -> bool:
    """Render Mermaid to PNG in headless Chromium (Playwright) with mermaid.js.

    Returns True if rendering succeeded, False otherwise.
    The .mmd file is always saved regardless.
    """
    from engine.utils.screenshot import is_available

    if not is_available():
        logger.info("Playwright not available — skipping Mermaid PNG render")
        return False

    page_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<script src="{_MERMAID_CDN}"></script>
<style>body {{ margin: 0; padding: 24px; background: white; }}</style>
</head><body>
<div id="out"></div>
<script>
  mermaid.initialize({{ startOnLoad: false, theme: {json.dumps(theme)} }});
  mermaid.render("diagram", {json.dumps(mermaid_text)})
    .then(r => {{ document.getElementById("out").innerHTML = r.svg; window.__done = "ok"; }})
    .catch(e => {{ window.__done = "error: " + e; }});
</script>
</body></html>"""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as f:
        f.write(page_html)
        temp_input = Path(f.name)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": 800}, device_scale_factor=2)
            page.goto(temp_input.resolve().as_uri())
            page.wait_for_function("window.__done !== undefined", timeout=30000)
            status = page.evaluate("window.__done")
            if status != "ok":
                logger.warning(f"Mermaid render failed: {status[:500]}")
                browser.close()
                return False
            output_path.parent.mkdir(parents=True, exist_ok=True)
            page.locator("#out svg").screenshot(path=str(output_path))
            browser.close()
        return True
    except Exception as e:
        logger.warning(f"Mermaid render error: {e}")
        return False
    finally:
        temp_input.unlink(missing_ok=True)
