"""Processor registry: Format → FormatProcessor mapping."""

from engine.models.enums import Format
from engine.processors.base import FormatProcessor
from engine.processors.branded_pdf_processor import BrandedPdfProcessor
from engine.processors.xls_processor import XlsProcessor
from engine.processors.html_processor import HtmlProcessor
from engine.processors.png_processor import PngProcessor
from engine.processors.mermaid_processor import MermaidProcessor
from engine.processors.pdf_processor import PdfProcessor
from engine.processors.chart_processor import ChartProcessor


# ─── Registry ────────────────────────────────────────────────────

PROCESSORS: dict[Format, FormatProcessor] = {
    Format.DOC: BrandedPdfProcessor(),    # Markdown → branded HTML → PDF
    Format.XLS: XlsProcessor(),
    Format.HTML: HtmlProcessor(),
    Format.PNG: PngProcessor(),
    Format.MERMAID: MermaidProcessor(),
    Format.PDF: PdfProcessor(),           # Raw HTML → PDF (used by FC2 lead magnet)
    Format.CHART: ChartProcessor(),
    # Format.SLIDES not yet implemented — low priority (1 doc only: FC3)
}


def get_processor(fmt: Format) -> FormatProcessor:
    """Get processor for a format. Raises KeyError if not implemented."""
    if fmt not in PROCESSORS:
        raise KeyError(
            f"No processor for format '{fmt.value}'. "
            f"Available: {[f.value for f in PROCESSORS]}"
        )
    return PROCESSORS[fmt]