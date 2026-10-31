from pathlib import Path

import pytest

from ytconv.config import Settings


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # Run from an empty dir so a developer's local .env can't change the result.
    monkeypatch.chdir(tmp_path)


def test_defaults_match_plan_limits() -> None:
    s = Settings()
    assert s.max_duration_seconds == 900
    assert s.retention_seconds == 3600


def test_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("YTCONV_MAX_DURATION_SECONDS", "60")
    assert Settings().max_duration_seconds == 60
