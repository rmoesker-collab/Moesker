#!/bin/bash
# StahlTrace SessionStart hook.
# Installs the Python toolchain so `uv run ruff`/`uv run pytest` work immediately
# in Claude Code on the web. Local sessions are left alone.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

if ! command -v uv >/dev/null 2>&1; then
  echo "session-start: uv not found on PATH; skipping dependency install" >&2
  exit 0
fi

# --frozen keeps uv.lock authoritative; the dev group carries pytest + ruff.
uv sync --frozen --all-groups

# stahltrace reads .env via pydantic-settings; make sure one exists so the CLI
# and config import cleanly without an interactive step.
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi
