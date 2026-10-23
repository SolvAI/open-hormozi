"""Preview images for the strategy page.

Each document is rendered once with Playwright and cached as JPEG files in
data/jobs/<id>/previews/. A branded report gives two A4 pages (its cover and
first page), a printable page gives one A4 page, a web page gives a 1120x700
browser view. Images (visuals, diagrams, charts) need no preview: the page
shows the file itself.

Rendering runs on one background thread that owns a Chromium instance and
closes it after a minute without requests.
"""

from __future__ import annotations

import itertools
import logging
import queue
import threading
from concurrent.futures import Future
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger("openhormozi.previews")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
A4 = {"width": 794, "height": 1123}   # CSS pixels at 96 dpi
WEB = {"width": 1120, "height": 700}
IDLE_CLOSE_S = 60

# Generated web pages can carry a cookie banner that would sit on the preview.
_HIDE_CSS = '[id*="cookie" i], [class*="cookie" i] { display: none !important; }'

# Lay the report's screen version out like the printed PDF: A4 width, no
# screen padding, the cover a full page.
_SHEET_CSS = """
html, body { background: #fff !important; }
body { padding: 0 !important; margin: 0 !important; display: block !important; min-height: 0 !important; }
.cover, .page { width: 794px !important; max-width: none !important; margin: 0 !important;
                box-shadow: none !important; border-radius: 0 !important; }
.cover { min-height: 1123px !important; }
.page { padding: 68px 60px !important; }
"""


def _source_html(path: Path) -> Path | None:
    if path.suffix == ".html":
        return path
    if path.suffix == ".pdf":
        html = path.with_suffix(".html")
        return html if html.exists() else None
    return None


@lru_cache(maxsize=1024)
def _is_report(html_path: str, _mtime_ns: int) -> bool:
    with open(html_path, encoding="utf-8", errors="ignore") as fh:
        return '<div class="cover-brand">' in fh.read()


def kind_of(path: Path) -> str | None:
    """How a deliverable previews: image, report, page, web, or None."""
    if path.suffix.lower() in IMAGE_EXTS:
        return "image"
    src = _source_html(path)
    if src is None:
        return None
    if _is_report(str(src), src.stat().st_mtime_ns):
        return "report"
    return "page" if path.suffix == ".pdf" else "web"


def part_count(kind: str | None) -> int:
    return {"report": 2, "page": 1, "web": 1}.get(kind or "", 0)


def _outputs(path: Path, kind: str) -> list[Path]:
    return [path.parent.parent / "previews" / f"{path.name}.{i}.jpg" for i in range(part_count(kind))]


def _fresh(path: Path, kind: str) -> bool:
    src_mtime = _source_html(path).stat().st_mtime
    return all(o.exists() and o.stat().st_mtime >= src_mtime for o in _outputs(path, kind))


def _failed_before(path: Path, kind: str) -> bool:
    return _failed.get(str(_outputs(path, kind)[0])) == _source_html(path).stat().st_mtime


def get(path: Path, kind: str, part: int) -> Path:
    """Path of the cached preview JPEG for one part of a file, rendering it first if needed."""
    if _failed_before(path, kind):
        raise RuntimeError(f"No preview for {path.name}")
    if not _fresh(path, kind):
        _renderer.submit(_source_html(path), kind, _outputs(path, kind), urgent=True).result(timeout=90)
    return _outputs(path, kind)[part]


def warm(paths: list[Path]) -> None:
    """Queue the previews that are missing or stale, in the given order, without waiting."""
    for path in paths:
        kind = kind_of(path)
        if part_count(kind) and not _fresh(path, kind) and not _failed_before(path, kind):
            _renderer.submit(_source_html(path), kind, _outputs(path, kind), urgent=False)


# Previews that failed, by output path → source mtime, so they aren't retried
# on every poll. A regenerated document gets a new mtime and a new attempt.
_failed: dict[str, float] = {}


class _Renderer:
    """One thread, one Chromium. Requests the page is waiting on go before warm-ups."""

    def __init__(self) -> None:
        self._queue: queue.PriorityQueue = queue.PriorityQueue()
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._jobs: dict[str, tuple] = {}   # key → (src, kind, outs, future)
        self._seq = itertools.count()

    def submit(self, src: Path, kind: str, outs: list[Path], urgent: bool) -> Future:
        key = str(outs[0])
        with self._lock:
            job = self._jobs.get(key)
            if job is None:
                job = self._jobs[key] = (src, kind, outs, Future())
                self._queue.put((1, next(self._seq), key))
            if urgent:
                # Queued again ahead of the warm-ups; the later copy is skipped.
                self._queue.put((0, next(self._seq), key))
            if self._thread is None:
                self._thread = threading.Thread(target=self._run, name="previews", daemon=True)
                self._thread.start()
            return job[3]

    def _run(self) -> None:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                browser = pw.chromium.launch()
                try:
                    self._serve(browser)
                finally:
                    browser.close()
        except Exception as e:  # Chromium missing or crashed: fail what's waiting
            logger.warning(f"Preview renderer stopped: {e}")
            with self._lock:
                self._thread = None
                for key, (src, *_, fut) in self._jobs.items():
                    _failed[key] = src.stat().st_mtime
                    fut.set_exception(e)
                self._jobs.clear()
                self._queue = queue.PriorityQueue()

    def _serve(self, browser) -> None:
        # One context per page size, kept open so web fonts load once.
        contexts = {
            "web": browser.new_context(viewport=WEB, device_scale_factor=1),
            "sheet": browser.new_context(viewport={"width": A4["width"], "height": 2 * A4["height"] + 100},
                                         device_scale_factor=0.75),
        }
        while True:
            try:
                _, _, key = self._queue.get(timeout=IDLE_CLOSE_S)
            except queue.Empty:
                with self._lock:
                    if self._queue.empty():
                        self._thread = None
                        return
                continue
            with self._lock:
                job = self._jobs.get(key)
            if job is None:
                continue
            src, kind, outs, fut = job
            try:
                outs[0].parent.mkdir(exist_ok=True)
                _render(contexts, src, kind, outs)
                fut.set_result(None)
            except Exception as e:
                logger.warning(f"Preview of {src.name} failed: {e}")
                _failed[key] = src.stat().st_mtime
                fut.set_exception(e)
            finally:
                with self._lock:
                    self._jobs.pop(key, None)


def _render(contexts: dict, src: Path, kind: str, outs: list[Path]) -> None:
    # The sheet context is tall enough to hold the cover and the first page one under the other.
    page = contexts["web" if kind == "web" else "sheet"].new_page()
    try:
        try:
            page.goto(src.resolve().as_uri(), wait_until="load", timeout=20000)
        except Exception as e:  # a slow web font shouldn't cost the preview
            logger.info(f"Preview of {src.name}: page still loading ({e}), capturing anyway")
        page.add_style_tag(content=_HIDE_CSS + (_SHEET_CSS if kind == "report" else ""))
        page.evaluate("document.fonts.ready.then(() => true)")
        shot = {"type": "jpeg", "quality": 82}
        if kind == "web":
            page.screenshot(path=str(outs[0]), **shot)
        elif kind == "page":
            page.screenshot(path=str(outs[0]), clip={"x": 0, "y": 0, **A4}, **shot)
        else:
            for out, selector in zip(outs, (".cover", ".page")):
                box = page.locator(selector).first.bounding_box()
                page.screenshot(path=str(out), clip={"x": box["x"], "y": box["y"], **A4}, **shot)
    finally:
        page.close()


_renderer = _Renderer()
