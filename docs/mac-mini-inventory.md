# Cloud workspace inventory

The work shown in the Claude sidebar on the Mac mini lives in the cloud, not on
that machine — the Mac mini is only the display. This document records what is
actually there, read from the live session and repository APIs on 2026-08-27,
and what state each item is in.

## Claude Code sessions

Nine sessions exist on the account. Five are the ungrouped entries at the top of
the sidebar; the two "Dispatch background conversation" rows are Cowork bridge
sessions with no repository attached.

| Session | Title | Branch | State |
| --- | --- | --- | --- |
| `session_018MHkRkdChKWBj6DSs848Cx` | Start StahlTrace agent project setup | `claude/init-stahltrace-project-jwkXx` | **default branch** — all current repo content came from here |
| `session_011FfRhHhaqiNJxq1rcXywXs` | Initial project setup and configuration | `claude/initial-setup-qtdWU` | never pushed — no commits exist |
| `session_01TPFAnM9AzNjsJUmBH8Gsuw` | Claude code installation | `claude/hopeful-darwin-8bjfi2` | never pushed — no commits exist |
| `session_01EM21nXx4TusWvdjrXZyHYR` | Fly dev, GitHub, and Stacktrace integration | `claude/fly-github-stacktrace-integration-tnpu87` | **2 commits, pushed, unmerged — imported by this branch** |
| `session_01LxqHrTSrbi2LJSUhXt7WJH` | Display discrepancy between devices | `claude/display-discrepancy-mac-mini-sk84kn` | never pushed — blocked awaiting a push from the Mac mini |
| `session_01Sk4qRVF9vfFwv5nPWQhwau` | Claude RC | `claude/claude-rc-yvc3zd` | never pushed — blocked on an unanswered question |
| `session_01Sd8kbMSchASkG8SF2WQRCn` | Dispatch background conversation | — | Cowork bridge, no repo |
| `session_01NKN5qi1g8XzZ6hn65nZY2t` | Dispatch background conversation | — | Cowork bridge, no repo |

Only three branches exist on `rmoesker-collab/Moesker`: the default branch, the
Fly/CI branch, and this import branch. The other session branches were never
pushed, so **no work is recoverable from them** — those sessions ended before
committing anything.

### Imported here

`claude/fly-github-stacktrace-integration-tnpu87` carried 409 lines that never
reached the default branch. This branch merges them:

- `fly.toml`, `Dockerfile`, `.dockerignore` — Fly.io deployment targeting the
  existing app `stahltrace-brain`
- `.github/workflows/ci.yml`, `.github/workflows/fly-deploy.yml` — CI and deploy
- `src/stahltrace/server.py` — HTTP server (new)
- `src/stahltrace/cli.py`, `src/stahltrace/db.py` — serve command and DB helpers
- `tests/test_smoke.py` — the repo's only tests
- `docs/deploy.md` — deployment runbook

## Repositories

| Repository | Visibility | Last push | Notes |
| --- | --- | --- | --- |
| `rmoesker-collab/Moesker` | public | 2026-08-27 | this repo — the StahlTrace substrate |
| `Stahltrace-Lda/stahltrace` | **private** | 2026-07-24 | separate org repo, push access — not yet examined |

`Stahltrace-Lda/stahltrace` is the likely home of the Threadweave / Synthesis /
CVM work. It could not be attached to this session: adding a repo from a
different owner than the session's existing sources is refused. Reaching it
requires **a new session started with `Stahltrace-Lda/stahltrace` as its initial
source**.

## Claude.ai projects — not machine-readable

The four grouped projects in the sidebar are claude.ai Projects, whose chats are
conversations rather than Claude Code sessions. No connector on this account
exposes conversation content (the connectors present are Gmail, Monte Carlo, and
Vercel), so these are recorded by title only:

- **`stahltrace`** — CVM substrate-input mode, Failed CVM, Private company
  document ingest, Soft deploy model, StahlTrace v7 autonomous system, Sibling
  Agent: Causal Value Map, Synthesis, Feeder sibling, Threadweave GitHub
  repository, v4 work, TES Synthedid CC
- **`stahltrace-cold-start-v4`** — StahlTrace cold start v4 SpaceX
- **`synthesis-cc`** — Synthesis agent output levels
- **`threadweave`** — Bayesian Update Agent

Getting their content into the repo requires exporting the conversations from
claude.ai and adding them here; nothing available to a session can pull them.

## Gaps against the repo

Even after the Fly/CI import, these threads have no code or docs in this repo:

- **v7 autonomous system** — the repo tops out at v6 (`docs/schema.md`,
  `stahltrace_v6_architecture.pdf`)
- **Threadweave**, **Causal Value Map / CVM**, **Synthesis siblings and feeders**,
  **Bayesian Update Agent** — no representation
- **Private document ingest** — `migrations/001_init.sql` defines `documents`
  with `vector(1536)`, but no ingest pipeline exists in `src/stahltrace/`
- **cold-start v4** — matching skills exist on the account, no in-repo runner

Check `Stahltrace-Lda/stahltrace` before rebuilding any of these.
