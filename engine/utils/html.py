"""HTML sanitization, template slot injection, and validation utilities."""

from __future__ import annotations

import re
import json
import logging
from pathlib import Path
from typing import Any
import json as _json

logger = logging.getLogger(__name__)

# ─── Slot injection ─────────────────────────────────────────────

_SLOT_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def inject_slots(html_template: str, data: dict[str, Any]) -> str:
    """Replace {{ slot_name }} placeholders in HTML with data values.

    Handles:
      - Simple string values: {{ headline }} → "Your Headline"
      - List values: {{ items }} → <li>item1</li><li>item2</li>
      - Missing slots: left as-is with a warning
    """
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        value = data.get(key)
        if value is None:
            logger.warning(f"HTML template slot '{key}' not found in data")
            return match.group(0)
        if isinstance(value, list):
            return "\n".join(f"<li>{_escape(v)}</li>" for v in value)
        return _escape(str(value))

    return _SLOT_PATTERN.sub(_replace, html_template)


def _escape(text: str) -> str:
    """Escape text for safe HTML insertion."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


# ─── Validation ─────────────────────────────────────────────────

def validate_html(html: str) -> list[str]:
    """Basic HTML validation. Returns list of issues (empty = ok)."""
    issues = []

    if not re.search(r"<html|<div|<body|<section", html, re.IGNORECASE):
        issues.append("No root HTML element found")

    # Check for unclosed tags (simple heuristic)
    open_tags = re.findall(r"<([a-zA-Z]\w*)[\s>]", html)
    close_tags = re.findall(r"</([a-zA-Z]\w*)>", html)
    self_closing = {"br", "hr", "img", "input", "meta", "link", "path", "circle", "rect"}

    open_counts: dict[str, int] = {}
    close_counts: dict[str, int] = {}
    for tag in open_tags:
        t = tag.lower()
        if t not in self_closing:
            open_counts[t] = open_counts.get(t, 0) + 1
    for tag in close_tags:
        t = tag.lower()
        close_counts[t] = close_counts.get(t, 0) + 1

    for tag, count in open_counts.items():
        closed = close_counts.get(tag, 0)
        if count > closed:
            issues.append(f"Potentially unclosed <{tag}> (opened {count}, closed {closed})")

    return issues


# ─── Markdown detection ─────────────────────────────────────────

# Content inside these tags is stripped before scanning —
# markdown syntax is legitimate inside code blocks, scripts, etc.
_SAFE_ZONE_PATTERNS = [
    re.compile(r"<pre\b[^>]*>.*?</pre>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<code\b[^>]*>.*?</code>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<style\b[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE),
]

# Markdown patterns that should have been converted to HTML
_MD_PATTERNS = {
    "headings": re.compile(r"^#{1,6} .+$", re.MULTILINE),
    "bold": re.compile(r"\*\*[^*\n]+\*\*"),
    "bullets": re.compile(r"^[\-\*] .+$", re.MULTILINE),
    "tables": re.compile(r"^\|.+\|$", re.MULTILINE),
    "code_fences": re.compile(r"^```\w*$", re.MULTILINE),
}

_MD_CHAR_THRESHOLD = 30


def detect_markdown_in_html(html: str) -> list[str]:
    """Detect markdown syntax that should have been converted to HTML.

    Strips safe zones (<pre>, <code>, <script>, <style>) before scanning
    so that legitimate markdown in code examples is not flagged.

    Returns list of issues if total markdown character count exceeds
    threshold.  Empty list = clean.
    """
    # Strip zones where markdown is legitimate
    cleaned = html
    for pattern in _SAFE_ZONE_PATTERNS:
        cleaned = pattern.sub("", cleaned)

    total_chars = 0
    found: dict[str, tuple[int, int]] = {}

    for name, pattern in _MD_PATTERNS.items():
        matches = pattern.findall(cleaned)
        if matches:
            chars = sum(len(m) for m in matches)
            total_chars += chars
            found[name] = (len(matches), chars)

    if total_chars <= _MD_CHAR_THRESHOLD:
        return []

    issues = []
    for name, (count, chars) in found.items():
        issues.append(f"{name}: {count} matches ({chars} chars)")
    issues.append(f"total: {total_chars} chars (threshold: {_MD_CHAR_THRESHOLD})")
    return issues


# ─── Wrapping ───────────────────────────────────────────────────

def ensure_full_document(html: str) -> str:
    """Wrap a fragment in a full HTML document if needed."""
    if re.search(r"<html", html, re.IGNORECASE):
        return html

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               margin: 0; padding: 24px; color: #1a1a1a; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""


# ─── JSON data injection (for complex templates) ────────────────

_JSON_MARKER = "__DATA_PLACEHOLDER__"


def load_and_inject(template_path: Path, data: dict[str, Any]) -> str:
    """Load an HTML template file and inject data.

    Supports two injection modes:
      1. {{ slot }} replacement for flat string/list values
      2. __DATA_PLACEHOLDER__ replacement for full JSON (complex templates)
    """
    if not template_path.exists():
        raise FileNotFoundError(f"HTML template not found: {template_path}")
    template = template_path.read_text(encoding="utf-8")

    # Mode 1: JSON data injection (for templates with JS rendering)
    if _JSON_MARKER in template:
        json_str = _json.dumps(data, ensure_ascii=False, indent=2)
        template = template.replace(_JSON_MARKER, json_str)

    # Mode 2: Slot injection (for templates with {{ }} placeholders)
    template = inject_slots(template, data)

    return template


# ─── LLM output extraction ─────────────────────────────────────

def extract_html_from_llm(text: str) -> str:
    """Extract HTML from LLM output that may include markdown preamble or fences.

    Handles:
      - Markdown commentary before ```html ... ``` fence
      - <!DOCTYPE> or <html> buried after prose
      - Plain ``` fences without language tag
    """
    stripped = text.strip()

    # 1. Find ```html fence (skip any markdown before it)
    for marker in ("```html", "```HTML"):
        idx = stripped.find(marker)
        if idx != -1:
            rest = stripped[idx + len(marker) :]
            end = rest.rfind("```")
            return rest[:end].strip() if end != -1 else rest.strip()

    # 2. Find HTML document start (strip markdown preamble)
    for tag in ("<!DOCTYPE", "<!doctype", "<html", "<HTML"):
        idx = stripped.find(tag)
        if idx > 0:
            return stripped[idx:]

    # 3. Standard ``` fence strip
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        if lines[-1].strip() == "```":
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        return "\n".join(lines).strip()

    return stripped