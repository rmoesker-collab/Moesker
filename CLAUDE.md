# StahlTrace — working notes for Claude

Agent-driven workflows backed by Postgres + pgvector. Python 3.11+, managed with `uv`.

## Commands

```bash
uv sync --frozen --all-groups   # install deps (dev group has pytest + ruff)
uv run ruff check .             # lint — must pass before commit
uv run ruff format .            # format (line-length 100, target py311)
uv run pytest                   # see "Tests" below
uv run stahltrace version       # CLI smoke check, needs no DB
uv run stahltrace db-check      # verifies connectivity + pgvector; needs Postgres up
docker compose up -d            # Postgres 16 + pgvector on :5432
```

`uv run stahltrace ask "..."` spends real API tokens. Don't run it to verify unrelated
changes — `version` and `db-check` cover the CLI wiring for free.

## Layout

```
src/stahltrace/
  config.py    pydantic-settings; reads .env, all fields have aliases (ANTHROPIC_API_KEY, ...)
  db.py        psycopg3 connection ctx manager + record_run helper
  agent.py     Claude Agent SDK wrapper (one-shot `query`)
  cli.py       Typer app; commands: version, ask, db-check
migrations/
  001_init.sql agent_runs + documents (vector(1536), hnsw cosine index)
docs/schema.md          twelve-table v6 trace substrate
src/stahltrace/stahltrace_v*_architecture.{md,pdf}   design docs, not code
```

## Conventions

- **Settings come from `config.py`, not `os.environ`.** Import `settings` and read the
  field; every value is aliased to an env var and defaulted there.
- **DB access goes through `db.get_conn()`.** It is a contextmanager that commits on
  clean exit and rolls back on exception. Don't open bare `psycopg.connect` calls.
  Rows come back as dicts (`row_factory=dict_row`).
- **Migrations are init-only.** `migrations/*.sql` is mounted at
  `/docker-entrypoint-initdb.d` and runs only on an empty volume. Changing an existing
  file does nothing to a live DB — add a new numbered file, and note that a rebuild
  needs `docker compose down -v`.
- Ruff is the only linter; there is no mypy config despite the code being typed.

## Tests

There is no test suite yet — `tests/` does not exist, so `uv run pytest` collects zero
tests and **exits 5**, not 0. That is the current expected state, not a failure you
introduced. If you add tests, put them in `tests/` at the repo root.

To verify a change today, use: `uv run ruff check .`, then
`uv run python -c "import stahltrace.cli"`, then `uv run stahltrace version`.

## Environment

`.env` is gitignored and is copied from `.env.example` by the SessionStart hook. It
holds `ANTHROPIC_API_KEY`, `DATABASE_URL`, and `STAHLTRACE_MODEL`. Never read, echo, or
commit `.env`; edit `.env.example` when a new setting needs documenting.

The default `STAHLTRACE_MODEL` in `.env.example` and `config.py` is `claude-sonnet-4-6`.
Note that the current default model recommendation is `claude-opus-5` — treat the pinned
value as deliberate unless asked to change it, and change both places together if so.
