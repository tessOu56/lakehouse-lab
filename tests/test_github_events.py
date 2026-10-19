from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from lakehouse_lab.assets.github_events import github_events_bronze

SAMPLE_EVENTS = [
    {
        "id": "1",
        "type": "PushEvent",
        "actor": {"login": "octocat"},
        "repo": {"name": "octocat/Hello-World"},
        "created_at": "2026-01-01T00:00:00Z",
    },
    {
        "id": "2",
        "type": "WatchEvent",
        "actor": {"login": "tess"},
        "repo": {"name": "tessOu56/lakehouse-lab"},
        "created_at": "2026-01-01T00:00:01Z",
    },
]


def test_github_events_bronze_writes_parquet_and_uploads(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    response = MagicMock()
    response.json.return_value = SAMPLE_EVENTS
    monkeypatch.setattr(
        "lakehouse_lab.assets.github_events.httpx.get",
        lambda *args, **kwargs: response,
    )

    s3 = MagicMock()
    monkeypatch.setattr(
        "lakehouse_lab.assets.github_events.boto3.client",
        lambda *args, **kwargs: s3,
    )
    result = github_events_bronze()

    out = Path("data/bronze/github_events/events.parquet")
    assert (tmp_path / out).is_file()
    df = pd.read_parquet(out)
    assert len(df) == 2
    assert list(df["id"]) == ["1", "2"]
    assert "type" in df.columns
    assert "actor.login" in df.columns
    assert "repo.name" in df.columns

    s3.upload_file.assert_called_once_with(
        str(out), "lakehouse", "bronze/github_events/events.parquet"
    )
    assert result.metadata["s3_uri"] == "s3://lakehouse/bronze/github_events/events.parquet"
    assert result.metadata["rows"] == 2
