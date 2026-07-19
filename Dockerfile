# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# claude-agent-sdk drives the Claude Code CLI, which needs Node.js at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm ca-certificates \
    && npm install -g @anthropic-ai/claude-code \
    && apt-get purge -y npm \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080
CMD ["stahltrace", "serve", "--host", "0.0.0.0", "--port", "8080"]
