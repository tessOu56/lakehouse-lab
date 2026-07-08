# lakehouse-lab

Public showcase: ingest **open data only** into a local medallion-style lakehouse (L0 bootstrap) — MinIO + Dagster + Parquet, built as a personal data-platform reference implementation.

**Red line**: open data only; no proprietary systems, business logic, or internal architecture reproduced here.

## L0 — what works today

- **MinIO** (S3-compatible) via Docker Compose
- **Dagster** asset: poll [GitHub public Events API](https://docs.github.com/en/rest/activity/events) → bronze Parquet under `data/bronze/github_events/`

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

## Roadmap

| Level | Focus |
|-------|--------|
| L0 | compose + GitHub Events → bronze (this repo) |
| L1 | batch + CDC streams, dbt silver/gold |
| L2 | FastAPI gold API + PWA dashboard |

Registry: `platform-command` → `lakehouse-lab` (role: showcase).
