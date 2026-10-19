import os
from pathlib import Path

import boto3
import httpx
import pandas as pd
from botocore.config import Config
from dagster import MaterializeResult, asset

BRONZE_DIR = Path("data/bronze/github_events")
BRONZE_OBJECT_KEY = "bronze/github_events/events.parquet"


def _minio_client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ.get("MINIO_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.environ.get("MINIO_ROOT_USER", "minioadmin"),
        aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin"),
        region_name="us-east-1",
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )


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

    bucket = os.environ.get("MINIO_BUCKET", "lakehouse")
    _minio_client().upload_file(str(out), bucket, BRONZE_OBJECT_KEY)

    return MaterializeResult(
        metadata={
            "rows": len(df),
            "path": str(out),
            "s3_uri": f"s3://{bucket}/{BRONZE_OBJECT_KEY}",
        }
    )
