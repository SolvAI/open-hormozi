"""Playwright-based HTML→PNG screenshot utility.

Used by PngProcessor and ChartProcessor.
Falls back gracefully if Playwright is not installed.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_PLAYWRIGHT_AVAILABLE: Optional[bool] = None


def is_available() -> bool:
    """Check if Playwright is installed and browsers are set up."""
    global _PLAYWRIGHT_AVAILABLE
    if _PLAYWRIGHT_AVAILABLE is not None:
        return _PLAYWRIGHT_AVAILABLE
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        _PLAYWRIGHT_AVAILABLE = True
    except Exception as e:
        logger.info(f"Playwright not available: {e}")
        _PLAYWRIGHT_AVAILABLE = False
    return _PLAYWRIGHT_AVAILABLE


def html_to_png(
    html_content: str,
    output_path: Path,
    width: int = 1200,
    height: int = 800,
    full_page: bool = False,
    scale: float = 2.0,
) -> bool:
    """Render HTML string to PNG via Playwright.

    Args:
        html_content: Complete HTML document string
        output_path: Where to save the PNG
        width: Viewport width in pixels
        height: Viewport height in pixels
        full_page: If True, capture entire page (ignore height)
        scale: Device scale factor (2.0 = retina)

    Returns:
        True if screenshot succeeded, False otherwise
    """
    if not is_available():
        logger.warning("Playwright not available — cannot generate PNG")
        return False

    try:
        from playwright.sync_api import sync_playwright

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html_content)
            temp_path = Path(f.name)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=scale,
            )
            page.goto(temp_path.resolve().as_uri())

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(
                path=str(output_path),
                full_page=full_page,
            )

            browser.close()

        temp_path.unlink(missing_ok=True)
        logger.info(f"Screenshot: {output_path} ({width}×{height} @{scale}x)")
        return True

    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        return False


def html_to_pdf(
    html_content: str,
    output_path: Path,
    format: str = "A4",
    print_background: bool = True,
    margin: Optional[dict] = None,
    viewport_width: int = 1280,
    header_template: Optional[str] = None,
    footer_template: Optional[str] = None,
) -> bool:
    """Render HTML to PDF via Playwright.

    Args:
        html_content: Complete HTML document string
        output_path: Where to save the PDF
        format: Paper format ('A4', 'Letter', etc.) — ignored when single_page=True
        print_background: Include background colors/images
        margin: Dict with top/right/bottom/left margins (e.g., {"top": "20mm"})
        viewport_width: Browser viewport width in pixels
        header_template: HTML for the running header. Chromium ignores CSS
            `@page` margin boxes, so page numbers must come through here using
            its `.pageNumber` / `.totalPages` span classes. Styles must be
            inline — the document's own CSS does not apply inside the template.
        footer_template: Same, for the running footer.

    Returns:
        True if rendering succeeded, False otherwise
    """
    if not is_available():
        logger.warning("Playwright not available — cannot generate PDF")
        return False

    if margin is None:
        margin = {"top": "15mm", "right": "15mm", "bottom": "15mm", "left": "15mm"}

    try:
        from playwright.sync_api import sync_playwright

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html_content)
            temp_path = Path(f.name)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={"width": viewport_width, "height": 900},
            )
            page.goto(temp_path.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            pdf_kwargs = dict(
                path=str(output_path),
                format=format,
                print_background=print_background,
                margin=margin,
            )
            if header_template is not None or footer_template is not None:
                # Chromium renders an empty box rather than nothing when only one
                # of the two is supplied, so always send both.
                pdf_kwargs.update(
                    display_header_footer=True,
                    header_template=header_template or "<span></span>",
                    footer_template=footer_template or "<span></span>",
                )

            page.pdf(**pdf_kwargs)
            logger.info(f"PDF: {output_path} ({format})")

            browser.close()

        temp_path.unlink(missing_ok=True)
        return True

    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        return False