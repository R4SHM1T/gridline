# Gridline. Plan and roadmap

> The repo-facing summary of where this project is going and how I'll know each phase is done.

## What

An IoT analytics platform on Samsung's SmartThings developer platform: device telemetry, Airflow-run ingestion, a dbt-modeled Postgres warehouse, Metabase dashboards, and an autopilot that reads anomaly flags from the warehouse and writes SmartThings rules back to the house.

## Goals

1. A real, verifiable Samsung integration: virtual devices, the devices REST API, the Rules engine.
2. Orchestration done properly: idempotent tasks, retries, backfills, alerts.
3. A layered dbt project (staging, intermediate, marts) with tests and published docs.
4. Automation with restraint: threshold rules, dry-run by default, allow-listed commands, an audit table of everything the autopilot does.

## Non-goals

- No physical hardware. Virtual devices plus a realism-tuned simulator, reproducible by anyone for free.
- No invented numbers. If a figure appears in this repo, a command reproduces it.
- Not a product. A working reference for how I'd build this properly.

## Data model

- Raw: `raw.device_events`, `raw.devices`
- Fleet (14 virtual devices): motion x3, contact x2, temperature x3, power plugs x3, bulbs x2, presence x1. Manifest in `config/fleet.yaml`.
- Marts: `fct_device_events`, `fct_energy_hourly`, `fct_room_activity_daily`, `dim_devices`, `mart_anomalies`, `mart_device_health`

## Roadmap. One phase, one PR, one tag

| Tag | Phase | State |
|---|---|---|
| v0.1.0 | Skeleton: scaffold, CI, docker-compose | done |
| v0.2.0 | Samsung handshake: fleet polling into raw tables | done |
| v0.3.0 | Simulator: daily rhythms, fault injection, unit tests | done |
| v0.4.0 | dbt: staging to marts, 25+ tests, published docs | building |
| v0.5.0 | Airflow: production DAG, retries, backfill runbook | building |
| v0.6.0 | Dashboards: Metabase boards, README captures | next |
| v0.7.0 | Autopilot: playbook rules, guardrails, audit table | next |
| v1.0.0 | Polish: demo capture, design notes, journal, writeup | next |

## Done means

- [ ] `make demo` boots the whole stack in one command
- [ ] Airflow DAG green end to end; a killed task recovers; a 7-day backfill works
- [ ] `dbt build` passes 25+ tests; docs site published
- [ ] Autopilot turns anomaly flags into tagged SmartThings rules (dry-run and live) with audit rows
- [ ] CI green on a fresh clone; no secrets anywhere in the repo
