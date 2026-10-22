"""File output utilities: disk writing, zip packaging, directory management."""

from __future__ import annotations

import json
import logging
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


def ensure_output_dir(base: Path, user_id: str, timestamp: Optional[datetime] = None) -> Path:
    """Create and return the output directory for a pipeline run.

    Structure: output/{user_id}_{timestamp}/
                ├── docs/
                ├── summaries/
                └── prompts/
    """
    ts = timestamp or datetime.utcnow()
    dir_name = f"{user_id}_{ts.strftime('%Y%m%d_%H%M%S')}"
    output_dir = base / dir_name

    for subdir in ("docs", "summaries", "prompts"):
        (output_dir / subdir).mkdir(parents=True, exist_ok=True)

    return output_dir


def write_json(path: Path, data: Any, indent: int = 2) -> Path:
    """Write JSON data to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=indent, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    logger.debug(f"Wrote JSON: {path}")
    return path


def write_text(path: Path, content: str) -> Path:
    """Write text content to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    logger.debug(f"Wrote text: {path}")
    return path


def package_zip(
    output_dir: Path,
    file_paths: list[Path],
    zip_name: Optional[str] = None,
) -> Path:
    """Package generated files into a ZIP archive.

    Args:
        output_dir: Root output directory (zip is created here)
        file_paths: All files to include
        zip_name: Optional custom name (default: directory name + .zip)

    Returns:
        Path to the created ZIP file
    """
    if not zip_name:
        zip_name = f"{output_dir.name}.zip"

    zip_path = output_dir / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in file_paths:
            if file_path.exists():
                try:
                    arcname = file_path.relative_to(output_dir)
                except ValueError:
                    arcname = file_path.name
                zf.write(file_path, arcname)
                logger.debug(f"Zipped: {arcname}")
            else:
                logger.warning(f"File not found for zip: {file_path}")

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    logger.info(f"Created ZIP: {zip_path} ({size_mb:.1f} MB, {len(file_paths)} files)")
    return zip_path


_HTML_PREFERRED_STEMS: set[str] = {
    "FC4_email_sequences",
    "u9_launch_roadmap_render",
}

_TIER_FOLDERS = {
    "U":  "1_Strategy",
    "CH": "2_Acquisition",
    "FC": "3_Funnel",
    "BM": "4_Operations",
    "MT": "5_Proof_and_Tools",
}


def _get_arcname(filename: str) -> str:
    """Map a filename to its subfolder in the ZIP."""
    upper = filename.upper()
    for prefix, folder in _TIER_FOLDERS.items():
        if upper.startswith(prefix):
            return f"{folder}/{filename}"
    return filename

def package_output(output_dir: Path) -> Path:
    """Package docs/ into a flat deliverable ZIP.

    Args:
        output_dir: Root output directory

    Excludes .mmd, intermediate .html (when same-stem .pdf exists),
    and swaps PDF→HTML for stems listed in _HTML_PREFERRED_STEMS.
    """
    files_to_zip: list[tuple[Path, str]] = []

    docs_dir = output_dir / "docs"
    if not docs_dir.exists():
        logger.warning("No docs directory found")
        return output_dir

    all_doc_files = [f for f in docs_dir.rglob("*") if f.is_file()]

    pdf_stems: set[str] = {f.stem for f in all_doc_files if f.suffix == ".pdf"}
    
    for f in all_doc_files:
        if f.suffix == ".mmd":
            continue

        if f.stem in _HTML_PREFERRED_STEMS:
            if f.suffix == ".pdf":
                continue
        elif f.suffix == ".html" and f.stem in pdf_stems:
            continue

        files_to_zip.append((f, f.name))

    if not files_to_zip:
        logger.warning("No files to package")
        return output_dir
    
    start_here = Path("templates/static_assets/0_START_HERE.pdf")
    if start_here.exists():
        files_to_zip.insert(0, (start_here, "0_START_HERE.pdf"))

    zip_path = output_dir / "strategy_pack.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path, arcname in files_to_zip:
            if file_path.exists():
                zf.write(file_path, _get_arcname(arcname))

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    logger.info(f"Created ZIP: {zip_path} ({size_mb:.1f} MB, {len(files_to_zip)} files)")
    return zip_path


def list_output_files(output_dir: Path) -> dict[str, list[str]]:
    """List all generated files grouped by subdirectory."""
    result: dict[str, list[str]] = {}
    for subdir in ("docs", "summaries", "prompts", "diagnostic"):
        path = output_dir / subdir
        if path.exists():
            files = sorted(f.name for f in path.rglob("*") if f.is_file())
            if files:
                result[subdir] = files
    root_files = sorted(
        f.name for f in output_dir.iterdir()
        if f.is_file() and f.suffix in (".json", ".zip")
    )
    if root_files:
        result["root"] = root_files
    return result