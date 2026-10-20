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
    }
]


def test_github_events_bronze_writes_local_parquet(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    response = MagicMock()
    response.json.return_value = SAMPLE_EVENTS
    monkeypatch.setattr(
        "lakehouse_lab.assets.github_events.httpx.get",
        lambda *args, **kwargs: response,
    )

    result = github_events_bronze()

    out = Path("data/bronze/github_events/events.parquet")
    assert (tmp_path / out).is_file()
    df = pd.read_parquet(out)
    assert len(df) == 1
    assert list(df["id"]) == ["1"]
    assert "actor.login" in df.columns
    assert result.metadata["rows"] == 1
    assert result.metadata["path"] == str(out)
