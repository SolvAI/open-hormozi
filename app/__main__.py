"""Start OpenHormozi: `python -m app` (the start scripts run this for you)."""

from __future__ import annotations

import argparse
import logging
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser

from app.paths import ROOT

# The engine resolves templates/ and config.yaml relative to the project root.
os.chdir(ROOT)

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

# Old Windows consoles can't print every character in the logs; never crash on it.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except AttributeError:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("openhormozi")


def ensure_browser() -> None:
    """Install Playwright's Chromium on first launch (it renders the PDFs)."""
    from engine.utils import screenshot

    if screenshot.is_available():
        return
    print("\nFirst launch: downloading the Chromium engine used to render PDFs (about 150 MB)...\n")
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
    screenshot._PLAYWRIGHT_AVAILABLE = None
    if not screenshot.is_available():
        hint = ""
        if sys.platform.startswith("linux"):
            hint = ("\n  On Linux, Chromium may need system libraries. Install them with:"
                    "\n    sudo .venv/bin/python -m playwright install-deps chromium")
        print(f"\n  WARNING: Chromium could not start, so PDFs and images can't be rendered.{hint}\n")


def find_port(host: str, preferred: int) -> int:
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return port
            except OSError:
                continue
    raise SystemExit(f"No free port between {preferred} and {preferred + 19}.")


def open_when_ready(url: str, host: str, port: int) -> None:
    def wait_and_open() -> None:
        for _ in range(100):
            try:
                with socket.create_connection((host, port), timeout=0.5):
                    break
            except OSError:
                time.sleep(0.2)
        webbrowser.open(url)

    threading.Thread(target=wait_and_open, daemon=True).start()


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenHormozi local app")
    parser.add_argument("--host", default=os.environ.get("OPENHORMOZI_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("OPENHORMOZI_PORT", "8765")))
    parser.add_argument("--no-browser", action="store_true", help="don't open a browser tab")
    args = parser.parse_args()

    ensure_browser()

    import uvicorn
    from app.server import app

    port = find_port(args.host, args.port)
    url = f"http://localhost:{port}"
    print(f"\n  OpenHormozi is running at {url}\n  Keep this window open while you generate. Press Ctrl+C to stop.\n", flush=True)
    if not args.no_browser:
        open_when_ready(url, "127.0.0.1" if args.host == "0.0.0.0" else args.host, port)
    uvicorn.run(app, host=args.host, port=port, log_level="warning")


if __name__ == "__main__":
    main()
