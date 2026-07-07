from pathlib import Path

import httpx
import pandas as pd
from dagster import MaterializeResult, asset

BRONZE_DIR = Path("data/bronze/github_events")


@asset(description="Poll GitHub public Events API → bronze Parquet (open data only)")
def github_events_bronze() -> MaterializeResult:
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    response = httpx.get(
        "https://api.github.com/events",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "lakehouse-lab-bootstrap",
        },
        timeout=30.0,
    )
    response.raise_for_status()
    events = response.json()
    df = pd.json_normalize(events)
    out = BRONZE_DIR / "events.parquet"
    df.to_parquet(out, index=False)
    return MaterializeResult(metadata={"rows": len(df), "path": str(out)})
