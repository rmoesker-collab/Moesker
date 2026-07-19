# Deploying StahlTrace to Fly.io (via GitHub)

StahlTrace ships with a `Dockerfile`, a `fly.toml`, and a GitHub Actions
workflow that deploys to Fly.io on every push to the default branch. Once the
one-time setup below is done, the loop is simply: **push to GitHub → CI runs →
Fly deploys → app live at `https://<app>.fly.dev`**.

## 1. One-time Fly.io setup

Install [flyctl](https://fly.io/docs/flyctl/install/) and sign in:

```bash
fly auth login
```

Create the app (uses the existing `fly.toml`; pick your own app name if
`stahltrace` is taken, and update `app = ...` in `fly.toml` to match):

```bash
fly launch --no-deploy --copy-config
```

### Postgres with pgvector

Create a Fly Managed Postgres cluster and attach it:

```bash
fly mpg create --name stahltrace-db --region ams
fly mpg attach stahltrace-db --app stahltrace
```

`attach` sets `DATABASE_URL` on the app automatically. Fly Managed Postgres
supports the `vector` extension; the app's release command
(`stahltrace db-migrate`) runs `CREATE EXTENSION IF NOT EXISTS vector` and the
rest of `migrations/*.sql` before each release goes live, so no manual schema
work is needed.

(Any external Postgres with pgvector — Neon, Supabase, RDS — also works: set
`DATABASE_URL` yourself with `fly secrets set DATABASE_URL=...`.)

### Secrets

```bash
fly secrets set ANTHROPIC_API_KEY=sk-ant-...
```

### First deploy (manual, to verify everything works)

```bash
fly deploy
curl https://stahltrace.fly.dev/health
curl https://stahltrace.fly.dev/health/db
```

## 2. One-time GitHub setup

Create a deploy token and add it to the repository so GitHub Actions can
deploy:

```bash
fly tokens create deploy --app stahltrace
```

Copy the output (including the `FlyV1 ` prefix) into the repository under
**Settings → Secrets and variables → Actions → New repository secret**, named
`FLY_API_TOKEN`.

That's it. From now on:

- `.github/workflows/ci.yml` — runs `ruff` + `pytest` on every push and PR.
- `.github/workflows/fly-deploy.yml` — deploys to Fly.io on every push to the
  default branch (it can also be run manually from the Actions tab via
  *Run workflow*).

If you later rename the default branch to `main`, the deploy workflow already
covers it; you can drop the old branch name from its `branches:` list.

## 3. Using the deployed app

The Fly deployment runs `stahltrace serve`, a small FastAPI wrapper around the
same agent used by the CLI:

| Endpoint     | Method | Description                                        |
| ------------ | ------ | -------------------------------------------------- |
| `/health`    | GET    | Liveness check (used by Fly health checks)         |
| `/health/db` | GET    | Verifies Postgres connectivity + pgvector          |
| `/ask`       | POST   | `{"prompt": "...", "system": null, "persist": true}` — runs the agent, records the run |

Example:

```bash
curl -X POST https://stahltrace.fly.dev/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize what StahlTrace is."}'
```

> **Note:** `/ask` is unauthenticated as shipped. Before exposing the app
> publicly, add an auth layer (e.g. a bearer-token check in
> `src/stahltrace/server.py`) or restrict the app to a private Fly network.

## Cost notes

`fly.toml` is configured with `auto_stop_machines` and
`min_machines_running = 0`, so the app machine suspends when idle and you only
pay for actual usage. The Postgres cluster runs continuously.
