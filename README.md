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

- **MinIO** (S3-compatible) via Docker Compose, bucket `lakehouse` created on `docker compose up`
- **Dagster** asset: poll GitHub public Events API → bronze Parquet at `data/bronze/github_events/` (local copy) and `s3://lakehouse/bronze/github_events/` (MinIO)

## Quick start

```bash
docker compose up -d
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
pip install -e ".[dev]"
dagster dev -f lakehouse_lab/definitions.py
```

Materialize asset `github_events_bronze` in the Dagster UI, then inspect:

```bash
ls data/bronze/github_events          # macOS / Linux
# dir data\bronze\github_events       # Windows
```

MinIO console: <http://localhost:9001> (user/password `minioadmin` / `minioadmin`, **dev-only**). Browse bucket `lakehouse` → `bronze/github_events/events.parquet`.

```bash
mc alias set local http://localhost:9000 minioadmin minioadmin
mc ls local/lakehouse/bronze/github_events/
```

| Setting | Dev value |
|---------|-----------|
| API | `http://localhost:9000` |
| Console | `http://localhost:9001` |
| Access key | `minioadmin` |
| Secret key | `minioadmin` |
| Bucket | `lakehouse` |
| Object | `bronze/github_events/events.parquet` |

## Tests

```bash
python -m pytest
```

L1+ (dbt silver/gold, gold API, dashboard) is **not implemented** in this repo.
