# Mac Mini — Claude workspace inventory

Transcribed from a photograph of the Claude desktop app sidebar on the Mac mini
(captured 2026-08-27). This is a **manual transcription of what was visible on
screen**, not a data export — no session content, timestamps, or message bodies
were available. Titles cut off by the sidebar width are marked with `…`.

Purpose: a checklist of the work threads living on the Mac mini, so they can be
prioritised and, where relevant, migrated into this repository.

## Sidebar navigation

`New` · `Routines` · `Dispatch (Beta)` · `Customize` · `More`

## Recent chats (ungrouped)

| Title | Notes |
| --- | --- |
| Display discrepancy between devi… | truncated — likely "between devices" |
| Fly dev, GitHub, and Stacktrace int… | truncated — likely "integration"; marked with a branch/PR icon |
| Claude code installation | |
| Start StahlTrace agent project setu… | truncated — likely "setup" |
| Initial project setup and configurat… | truncated — likely "configuration" |

## Project: `stahltrace`

| Title | Notes |
| --- | --- |
| CVM substrate-input mode for Th… | truncated — likely "for Threadweave" |
| Failed CVM | |
| Private company document ingest… | truncated — likely "ingestion" |
| Soft deploy model for StahlTrace | marked with a green branch/PR icon (active branch?) |
| StahlTrace v7 autonomous system | |
| Sibling Agent: Causal Value Map | marked with a red branch/PR icon (failed/closed?) |
| Synthesis | |
| Feeder sibling under StahlTrace | |
| Threadweave GitHub repository | |
| v4 work | |
| TES Synthedid CC | transcription uncertain — "Synthedid" may be misread |

## Project: `stahltrace-cold-start-v4`

| Title | Notes |
| --- | --- |
| StahlTrace cold start v4 SpaceX | |

## Project: `synthesis-cc`

| Title | Notes |
| --- | --- |
| Synthesis agent output levels | |

## Project: `threadweave`

| Title | Notes |
| --- | --- |
| Bayesian Update Agent | |

## Account

Signed in as **Ronald** (Max plan). The app was showing a
"For your security, sign in again to keep using C…" re-authentication banner.

## Relationship to this repository

This repo (`moesker`) currently holds the StahlTrace substrate:

- `README.md` — Python 3.11 + uv, Claude Agent SDK, Postgres 16 + pgvector, Typer CLI
- `docs/schema.md` — twelve-table trace substrate (v6)
- `src/stahltrace/stahltrace_v4_architecture.md` / `.pdf`, `stahltrace_v6_architecture.pdf`
- `migrations/001_init.sql` — `agent_runs` + `documents` with `vector(1536)`

Threads above that plausibly map onto repo work and are **not yet represented here**:

- **v7 autonomous system** — no v7 architecture doc exists; repo tops out at v6
- **Threadweave** — referenced in two chat titles and one project, no code or docs in-repo
- **Causal Value Map / CVM** — three chats (incl. one "Failed"), nothing in-repo
- **Synthesis / synthesis-cc / feeder sibling** — sibling-agent design, nothing in-repo
- **Bayesian Update Agent** — nothing in-repo
- **Private company document ingest** — relates to `documents` + pgvector, but no ingest pipeline exists in `src/stahltrace/`
- **cold-start v4** — matches the `stahltrace-cold-start*` skills, no in-repo runner

## Importing the actual content

Nothing beyond these titles can be recovered from a photo. To bring the real
material across, export it on the Mac mini and add it to this branch — for
example, conversation exports from the Claude app, or any local project
directories (`threadweave`, `synthesis`) pushed as a branch or attached
directly. The content can then be parsed and landed in the repo properly.
