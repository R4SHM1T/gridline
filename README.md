# Gridline

![Hero Image](https://via.placeholder.com/800x400?text=Gridline+Analytics)

Warehouse-grade analytics for a Samsung smart home: SmartThings telemetry → Airflow-orchestrated EL → dbt-modeled warehouse → dashboards → an AI agent that turns insights back into SmartThings automations.

## Why this exists

Every portfolio pipeline I'd seen — including my own early ones — ran on dead CSVs. Static datasets can't teach you what actually breaks pipelines in production: late-arriving events, flaky sensors, rate limits, schema drift. I wanted a source that *behaves* like production. Smart-home telemetry fit perfectly, but I wasn't going to buy a fleet of devices to learn on — and that's when I found that Samsung's SmartThings is the one major smart-home platform with a fully open developer surface: virtual devices that behave like real ones, real API payloads, real rate limits, a real rules engine. So the warehouse got built on Samsung's rails — and once telemetry was flowing, the obvious next step was closing the loop: let an agent act back on the home through the same API the data came from.

## The Closed Loop

Most portfolio pipelines stop at a dashboard; this one closes the loop. Data flows OUT of the home into a warehouse, and decisions flow BACK into the home via the SmartThings Rules API. Ingest → model → decide → actuate.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/r4shm1t/gridline.git
cd gridline

# 2. Setup your .env file
cp .env.example .env
# Edit .env and add your SmartThings PAT

# 3. Boot the stack
make demo
```

## Architecture

![Architecture](https://via.placeholder.com/800x400?text=Architecture+Diagram)
The pipeline is orchestrated with Airflow. Raw data lands in Postgres, gets transformed by dbt, and visualized in Metabase.

## Honest Scope: What I used vs What I built
- **Simulated vs Real**: No physical hardware: devices are **SmartThings virtual devices** fed by a realism-tuned simulator. This makes the project reproducible without requiring actual hardware.
- **Metrics**: No invented usage metrics. Benchmarks only for things actually measured.
- Not a product; a reference implementation.

## What I'd Do Next
- Swap local Postgres for Snowflake or BigQuery.
- Migrate batch EL to streaming with Kafka for real-time anomaly detection.
