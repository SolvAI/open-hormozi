"""Chart processor: Chart.js JSON → HTML → PNG screenshot.

Renders Chart.js configuration into a self-contained HTML page,
then screenshots it to PNG.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from engine.processors.base import FormatProcessor
from engine.utils.screenshot import html_to_png, is_available as playwright_available

logger = logging.getLogger(__name__)

# Chart.js CDN (pinned version for reproducibility)
_CHARTJS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"


class ChartProcessor(FormatProcessor):
    """Render Chart.js JSON config to PNG.

    1. Parse LLM JSON output as Chart.js config
    2. Wrap in self-contained HTML with <canvas>
    3. Screenshot to PNG via Playwright
    4. Fallback: save HTML for manual viewing
    """

    def __init__(self, width: int = 1000, height: int = 600):
        self.width = width
        self.height = height

    def process(
        self,
        content: Any,
        doc_id: str,
        output_dir: Path,
        template_path: str | None = None,
        metadata: dict | None = None,
    ) -> Path:
        self._ensure_dir(output_dir)

        # Build explicit filename from doc_name
        doc_name = (metadata or {}).get("doc_name", doc_id)
        slug = doc_id.lower()
        name_slug = self._slugify(doc_name)
        base_name = f"{slug}_{name_slug}_chart"

        # Parse chart config
        chart_config = self._ensure_dict(content)
        chart_json = json.dumps(chart_config, ensure_ascii=False)

        # Build self-contained HTML
        html = self._build_chart_html(chart_json)

        # Try PNG screenshot
        png_path = output_dir / f"{base_name}.png"

        if playwright_available():
            success = html_to_png(
                html, png_path,
                width=self.width, height=self.height,
            )
            if success:
                return png_path

        # Fallback: save HTML
        logger.warning(
            f"ChartProcessor [{doc_id}]: Playwright unavailable. Saving HTML."
        )
        html_path = output_dir / f"{base_name}.html"
        html_path.write_text(html, encoding="utf-8")
        return html_path

    def _build_chart_html(self, chart_json: str) -> str:
        """Build a self-contained HTML page with Chart.js."""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="{_CHARTJS_CDN}"></script>
    <style>
        body {{
            margin: 0;
            padding: 24px;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        .chart-container {{
            width: {self.width - 48}px;
            height: {self.height - 48}px;
            position: relative;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <canvas id="chart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('chart').getContext('2d');
        const config = {chart_json};
        new Chart(ctx, config);
    </script>
</body>
</html>"""

    def _ensure_dict(self, content: Any) -> dict:
        if isinstance(content, dict):
            return content
        if isinstance(content, str):
            text = content.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[-1].strip() == "```":
                    lines = lines[1:-1]
                else:
                    lines = lines[1:]
                text = "\n".join(lines).strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                logger.error(f"ChartProcessor: invalid JSON chart config")
                return {
                    "type": "bar",
                    "data": {
                        "labels": ["Error"],
                        "datasets": [{"label": "Parse Error", "data": [0]}],
                    },
                }
        return {"type": "bar", "data": {"labels": [], "datasets": []}}