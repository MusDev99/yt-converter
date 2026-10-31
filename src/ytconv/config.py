"""Settings from YTCONV_* environment variables (see .env.example)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="YTCONV_", env_file=".env", extra="ignore")

    max_duration_seconds: int = 900
    audio_bitrate_kbps: Literal[128, 192, 256, 320] = 192
    download_dir: Path = Path("/tmp/ytconv")  # noqa: S108 - container scratch dir, wiped by retention
    retention_seconds: int = 3600


@lru_cache
def get_settings() -> Settings:
    return Settings()
