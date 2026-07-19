# StahlTrace

Agent-driven workflows backed by Postgres + pgvector.

## Stack

- **Python 3.11+** managed with [uv](https://github.com/astral-sh/uv)
- **Claude Agent SDK** for agent orchestration
- **Postgres 16 + pgvector** running in Docker
- **Typer** CLI (`stahltrace ...`)

## Quickstart

```bash
# 1. Install deps
uv sync

# 2. Bring up Postgres (auto-runs migrations/001_init.sql on first boot)
docker compose up -d

# 3. Configure secrets
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY

# 4. Sanity-check the DB
uv run stahltrace db-check

# 5. Ask the agent something
uv run stahltrace ask "Summarize what StahlTrace is."
```

## Layout

```
src/stahltrace/
  config.py    pydantic-settings, reads .env
  db.py        psycopg connection + run-recording + migration helpers
  agent.py     Claude Agent SDK wrapper
  cli.py       Typer entry point
  server.py    FastAPI wrapper (`stahltrace serve`) for the Fly.io deployment
migrations/
  001_init.sql  agent_runs + documents (with vector(1536))
docker-compose.yml
Dockerfile      production image (used by Fly.io)
fly.toml        Fly.io app config
```

## Deployment

The repo is wired for **GitHub → Fly.io** continuous deployment: CI
(`ruff` + `pytest`) runs on every push, and pushes to the default branch
deploy to Fly.io automatically. See [docs/deploy.md](docs/deploy.md) for the
one-time setup (Fly app, Managed Postgres with pgvector, `FLY_API_TOKEN`
secret).

## Development

```bash
uv run ruff check .
uv run pytest
```
