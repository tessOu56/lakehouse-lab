# lakehouse-lab

Local **L0 bronze** lab: ingest **open data only** into MinIO + Dagster + Parquet. Not a production data platform.

## What this proves

| Proof | Honest bound |
|-------|----------------|
| **L0 bronze** | Docker Compose MinIO + one Dagster asset → bronze Parquet |
| **Open data only** | [GitHub public Events API](https://docs.github.com/en/rest/activity/events). No employer, proprietary, or production datasets |
| **Not claimed** | No silver/gold pipeline, no hosted warehouse, no production data platform |

**Red line:** open data only; no proprietary systems, business logic, or internal architecture reproduced here.

## L0 — what works today

- **MinIO** (S3-compatible) via Docker Compose
- **Dagster** asset: poll GitHub public Events API → bronze Parquet under `data/bronze/github_events/`

## Quick start

```bash
docker compose up -d
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
dagster dev -f lakehouse_lab/definitions.py
```

Materialize asset `github_events_bronze` in the Dagster UI, then inspect:

```bash
dir data\bronze\github_events
```

L1+ (dbt silver/gold, gold API, dashboard) is **not implemented** in this repo.
