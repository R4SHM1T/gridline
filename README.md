# Gridline

Warehouse-grade analytics for a Samsung smart home: SmartThings telemetry → Airflow-orchestrated EL → dbt-modeled warehouse → dashboards → an AI agent that turns insights back into SmartThings automations.

## The Closed Loop

Most portfolio pipelines stop at a dashboard; this one closes the loop. Data flows OUT of the home into a warehouse, and decisions flow BACK into the home via the SmartThings Rules API. Ingest → model → decide → actuate.

## Quickstart
*(To be populated in later phases)*

## Architecture
*(To be populated in later phases)*

## Honest Scope
- No physical hardware: devices are **SmartThings virtual devices** fed by a realism-tuned simulator.
- No invented usage metrics. Benchmarks only for things actually measured.
- Not a product; a reference implementation.

## What I'd Do Next
*(To be populated in later phases)*
