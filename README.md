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
  db.py        psycopg connection + run-recording helpers
  agent.py     Claude Agent SDK wrapper
  cli.py       Typer entry point
migrations/
  001_init.sql  agent_runs + documents (with vector(1536))
docker-compose.yml
```

## Development

```bash
uv run ruff check .
uv run pytest
```
