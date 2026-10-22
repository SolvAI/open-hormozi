#!/usr/bin/env bash
# OpenHormozi launcher for macOS and Linux.
# Installs uv (which brings its own Python) on first run, then starts the app.
set -euo pipefail
cd "$(dirname "$0")"

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv, the Python package manager (one time, about 30 MB)..."
  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://astral.sh/uv/install.sh | sh
  else
    echo "Neither curl nor wget is installed. Install one of them, or install uv from https://docs.astral.sh/uv/ and run this script again."
    exit 1
  fi
fi

exec uv run --frozen python -m app "$@"
