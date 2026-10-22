"""Markdown parsing utilities for section extraction and heading analysis.

Used by summarizer and context_builder to extract specific sections
from generated markdown documents.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class MarkdownSection:
    """One section of a markdown document."""
    heading: str
    level: int          # 1 = #, 2 = ##, etc.
    content: str        # everything between this heading and the next same-or-higher level
    start_line: int
    end_line: int


_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def extract_sections(markdown: str) -> list[MarkdownSection]:
    """Parse markdown into a list of sections by heading.

    Each section contains everything from its heading until the next
    heading of the same or higher level (or end of document).
    """
    lines = markdown.split("\n")
    headings: list[tuple[int, str, int]] = []  # (level, text, line_number)

    for i, line in enumerate(lines):
        match = _HEADING_PATTERN.match(line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((level, text, i))

    if not headings:
        return [MarkdownSection(
            heading="(document)",
            level=0,
            content=markdown,
            start_line=0,
            end_line=len(lines),
        )]

    sections = []
    for idx, (level, text, start) in enumerate(headings):
        # Find end: next heading at same or higher level
        end = len(lines)
        for next_level, _, next_start in headings[idx + 1:]:
            if next_level <= level:
                end = next_start
                break

        content = "\n".join(lines[start:end]).strip()
        sections.append(MarkdownSection(
            heading=text,
            level=level,
            content=content,
            start_line=start,
            end_line=end,
        ))

    return sections


def get_section(markdown: str, heading: str) -> Optional[str]:
    """Extract a specific section by heading text (case-insensitive)."""
    for section in extract_sections(markdown):
        if section.heading.lower() == heading.lower():
            return section.content
    return None


def get_sections_at_level(markdown: str, level: int) -> list[MarkdownSection]:
    """Get all sections at a specific heading level."""
    return [s for s in extract_sections(markdown) if s.level == level]


def strip_headings(markdown: str) -> str:
    """Remove all heading markers, leaving plain text."""
    return _HEADING_PATTERN.sub(r"\2", markdown)


def truncate_to_sections(markdown: str, max_sections: int = 3) -> str:
    """Keep only the first N top-level sections (for summarization)."""
    sections = extract_sections(markdown)
    if not sections:
        return markdown

    top_level = sections[0].level
    top_sections = [s for s in sections if s.level == top_level]

    if len(top_sections) <= max_sections:
        return markdown

    # Return up to the start of the (max_sections+1)th section
    cutoff = top_sections[max_sections].start_line
    lines = markdown.split("\n")
    return "\n".join(lines[:cutoff]).strip()