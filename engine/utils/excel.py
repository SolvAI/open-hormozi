"""openpyxl helper utilities for building and populating XLSX files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

logger = logging.getLogger(__name__)

# ─── Predefined styles ──────────────────────────────────────────

HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
HEADER_FILL = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
HEADER_ALIGNMENT = Alignment(horizontal="center", vertical="center", wrap_text=True)

SUBHEADER_FONT = Font(name="Calibri", size=10, bold=True, color="2C3E50")
SUBHEADER_FILL = PatternFill(start_color="ECF0F1", end_color="ECF0F1", fill_type="solid")

BODY_FONT = Font(name="Calibri", size=10)
BODY_ALIGNMENT = Alignment(vertical="top", wrap_text=True)

USER_INPUT_FILL = PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style="thin", color="BDC3C7"),
    right=Side(style="thin", color="BDC3C7"),
    top=Side(style="thin", color="BDC3C7"),
    bottom=Side(style="thin", color="BDC3C7"),
)

STYLE_MAP = {
    "bold_header": {"font": HEADER_FONT, "fill": HEADER_FILL, "alignment": HEADER_ALIGNMENT},
    "subheader": {"font": SUBHEADER_FONT, "fill": SUBHEADER_FILL},
    "user_input": {"fill": USER_INPUT_FILL},
}


def create_workbook_from_json(data: dict) -> Workbook:
    """Create a styled XLSX workbook from JSON structure.

    Expected JSON:
    {
      "sheets": [
        {
          "name": "Sheet Name",
          "headers": ["Col A", "Col B", ...],
          "rows": [["val1", "val2"], ...],
          "formulas": {"C2": "=A2*B2", ...},       # optional
          "formatting": {"A1:B1": "bold_header"}   # optional
          "column_widths": {"A": 20, "B": 35}      # optional
        }
      ]
    }
    """
    wb = Workbook()
    # Remove default sheet
    if wb.active and len(data.get("sheets", [])) > 0:
        wb.remove(wb.active)

    sheets = data.get("sheets", [])
    if not sheets:
        logger.warning("No sheets in JSON data — creating empty workbook")
        return wb

    for sheet_data in sheets:
        ws = wb.create_sheet(title=sheet_data.get("name", "Sheet")[:31])

        # ── Headers ──
        headers = sheet_data.get("headers", [])
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL
            cell.alignment = HEADER_ALIGNMENT
            cell.border = THIN_BORDER

        # ── Rows ──
        rows = sheet_data.get("rows", [])
        for row_idx, row_data in enumerate(rows, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.border = THIN_BORDER
                cell.alignment = BODY_ALIGNMENT
                cell.font = BODY_FONT

                # Handle [USER INPUT] markers
                if isinstance(value, str) and "[USER INPUT]" in value.upper():
                    cell.value = value
                    cell.fill = USER_INPUT_FILL
                else:
                    cell.value = _coerce_value(value)

        # ── Formulas ──
        formulas = sheet_data.get("formulas", {})
        for cell_ref, formula in formulas.items():
            ws[cell_ref] = formula

        # ── Formatting ──
        formatting = sheet_data.get("formatting", {})
        for cell_range, style_name in formatting.items():
            apply_style_range(ws, cell_range, style_name)

        # ── Column widths ──
        col_widths = sheet_data.get("column_widths", {})
        if col_widths:
            for col_letter, width in col_widths.items():
                ws.column_dimensions[col_letter].width = width
        else:
            _auto_width(ws, headers, rows)

        # Freeze top row
        ws.freeze_panes = "A2"

    return wb


def inject_into_template(
    template_path: Path,
    data: dict,
    sheet_name: Optional[str] = None,
) -> Workbook:
    """Load an existing XLSX template and inject data into marked cells.

    Looks for cells containing {{key}} and replaces with data[key].
    Also processes rows/formulas if "injections" key exists in data.
    """
    wb = load_workbook(str(template_path))
    ws = wb[sheet_name] if sheet_name else wb.active

    # Simple slot replacement
    slots = data.get("slots", data)
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "{{" in cell.value:
                for key, value in slots.items():
                    placeholder = "{{" + key + "}}"
                    if placeholder in cell.value:
                        if cell.value.strip() == placeholder:
                            cell.value = _coerce_value(value)
                        else:
                            cell.value = cell.value.replace(placeholder, str(value))

    # Row injection (for data tables within the template)
    injections = data.get("row_injections", [])
    for injection in injections:
        sheet = wb[injection.get("sheet", ws.title)]
        start_row = injection.get("start_row", 2)
        for row_offset, row_data in enumerate(injection.get("rows", [])):
            for col_idx, value in enumerate(row_data, 1):
                if value is None:
                    continue  # Skip null — preserve existing content/formulas
                cell = sheet.cell(row=start_row + row_offset, column=col_idx)
                cell.value = _coerce_value(value)

    return wb

def apply_style_range(ws, cell_range: str, style_name: str):
    """Apply a predefined style to a cell range."""
    style = STYLE_MAP.get(style_name, {})
    if not style:
        logger.warning(f"Unknown style '{style_name}'")
        return

    from openpyxl.utils import range_boundaries
    try:
        min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    except Exception:
        # Single cell
        cell = ws[cell_range]
        for attr, val in style.items():
            setattr(cell, attr, val)
        return

    for row in ws.iter_rows(
        min_row=min_row, max_row=max_row,
        min_col=min_col, max_col=max_col,
    ):
        for cell in row:
            for attr, val in style.items():
                setattr(cell, attr, val)


def _coerce_value(value: Any) -> Any:
    """Coerce string values to numbers where appropriate."""
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    # Try int
    try:
        return int(stripped)
    except ValueError:
        pass
    # Try float (handle both . and , as decimal separator)
    try:
        return float(stripped.replace(",", "."))
    except ValueError:
        pass
    return value


def _auto_width(ws, headers: list, rows: list):
    """Set column widths based on content length (heuristic)."""
    for col_idx in range(1, len(headers) + 1):
        max_len = len(str(headers[col_idx - 1])) if col_idx <= len(headers) else 8
        for row_data in rows:
            if col_idx <= len(row_data):
                cell_len = len(str(row_data[col_idx - 1]))
                max_len = max(max_len, cell_len)
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = min(max_len + 4, 60)