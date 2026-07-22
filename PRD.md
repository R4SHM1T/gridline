# GRIDLINE — PRD (trimmed)

> Full development guide lives in my planning docs; this is the repo-facing summary.

## What

An end-to-end IoT analytics platform on **Samsung SmartThings**: telemetry → Airflow-orchestrated EL → dbt-modeled Postgres warehouse → Metabase dashboards → a guard-railed AI agent that reads the warehouse and writes SmartThings automations via the Rules API.

## Goals

1. Real, verifiable Samsung integration (SmartThings API, virtual devices, Rules API).
2. Orchestration done properly: idempotent tasks, retries, backfills, alerts.
3. Analytics engineering: layered dbt project (staging → intermediate → marts) with tests + published docs.
4. Applied AI: tool-calling agent with dry-run default, allow-listed commands, and an audit table.

## Non-goals

- No physical hardware — virtual devices + a realism-tuned simulator (reproducible by anyone, free).
- No invented metrics. If a number appears in this repo, a command reproduces it.
- Not a product; a reference implementation.

## Data model

- **Raw:** `raw.device_events`, `raw.devices`
- **Fleet (14 virtual devices):** motion ×3, contact ×2, temp ×3, power plugs ×3, bulbs ×2, presence ×1 — manifest in `config/fleet.yaml`
- **Marts:** `fct_device_events`, `fct_energy_hourly`, `fct_room_activity_daily`, `dim_devices`, `mart_anomalies`, `mart_device_health`

## Roadmap (one phase = one PR = one tag)

| Tag | Phase | State |
|---|---|---|
| v0.1.0 | Skeleton: scaffold, CI, docker-compose | ✅ |
| v0.2.0 | Samsung handshake: fleet polling → raw landing | ✅ |
| v0.3.0 | Simulator: daily rhythms + anomaly injection, unit tests | ✅ |
| v0.4.0 | dbt: staging → intermediate → marts, ≥25 tests, docs | 🚧 |
| v0.5.0 | Airflow: production DAG, retries, backfill runbook | 🚧 |
| v0.6.0 | Dashboards: Metabase boards + README captures | 🖜 |
| v0.7.0 | Agent: tools, guardrails, audit, demo transcript | 🖜 |
| v1.0.0 | Polish: hero GIF, ADRs, journal, writeup | 🖜 |

## Acceptance criteria for v1.0

- [ ] `make demo` boots the whole stack with one command
- [ ] Airflow DAG green end-to-end; killed task recovers; 7-day backfill works
- [ ] `dbt build` passes ≥ 25 tests; docs site published
- [ ] Agent answers warehouse questions and creates tagged SmartThings rules (dry-run + live) with audit rows
- [ ] CI green on fresh clone; no secrets in repo
