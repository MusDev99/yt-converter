"""Probe a video and convert its audio to MP3 with yt-dlp + ffmpeg.

yt-dlp is driven through its Python API (never a shell). The downloader is
injectable so tests never touch YouTube.
"""

import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, cast

import yt_dlp

from ytconv.naming import mp3_filename
from ytconv.urls import canonical_url

log = logging.getLogger(__name__)


class ConvertError(RuntimeError):
    """Short, user-safe reason the convert failed; details are logged."""


class Downloader(Protocol):
    def extract_info(self, url: str, download: bool = ...) -> Any: ...  # yt-dlp returns a dict
    def __enter__(self) -> "Downloader": ...
    def __exit__(self, *exc: object) -> None: ...


DownloaderFactory = Callable[[Mapping[str, Any]], Downloader]


def _default_factory(opts: Mapping[str, Any]) -> Downloader:
    return cast(Downloader, yt_dlp.YoutubeDL(dict(opts)))


@dataclass(frozen=True)
class VideoInfo:
    video_id: str
    title: str
    uploader: str
    duration_seconds: int
    license: str | None

    @property
    def is_creative_commons(self) -> bool:
        return bool(self.license and "creative commons" in self.license.lower())


@dataclass(frozen=True)
class ConvertResult:
    info: VideoInfo
    path: Path
    filename: str  # suggested download name


_BASE_OPTS: dict[str, Any] = {
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "noprogress": True,
    "restrictfilenames": True,
    "logger": log,  # route yt-dlp output into our log, never to the user
}


def _info_from(raw: Mapping[str, Any], video_id: str) -> VideoInfo:
    if raw.get("is_live") or raw.get("live_status") in {"is_live", "is_upcoming"}:
        raise ConvertError("Live streams can't be converted.")
    duration = raw.get("duration")
    if not isinstance(duration, int | float) or duration <= 0:
        raise ConvertError("Couldn't read the video length.")
    return VideoInfo(
        video_id=video_id,
        title=str(raw.get("title") or video_id),
        uploader=str(raw.get("uploader") or raw.get("channel") or ""),
        duration_seconds=int(duration),
        license=str(raw["license"]) if raw.get("license") else None,
    )


def probe(video_id: str, *, factory: DownloaderFactory | None = None) -> VideoInfo:
    """Read title, length and licence without downloading."""
    try:
        with (factory or _default_factory)({**_BASE_OPTS, "skip_download": True}) as ydl:
            raw = ydl.extract_info(canonical_url(video_id), download=False)
    except yt_dlp.utils.DownloadError as exc:
        log.warning("probe failed for %s: %s", video_id, exc)
        raise ConvertError("YouTube didn't return this video. It may be private.") from exc
    return _info_from(raw, video_id)


def check_duration(info: VideoInfo, max_seconds: int) -> None:
    if info.duration_seconds > max_seconds:
        raise ConvertError(f"Video is longer than the {max_seconds // 60}-minute limit.")


def convert(
    info: VideoInfo,
    out_dir: Path,
    *,
    bitrate_kbps: int,
    max_seconds: int,
    factory: DownloaderFactory | None = None,
) -> ConvertResult:
    """Download best audio and encode it to MP3 with title/artist tags."""
    check_duration(info, max_seconds)
    out_dir.mkdir(parents=True, exist_ok=True)
    opts = {
        **_BASE_OPTS,
        "format": "bestaudio/best",
        # File named by id so a title can never pick the path.
        "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
        # Second guard in case the length changed between probe and download.
        "match_filter": yt_dlp.utils.match_filter_func(f"duration <= {max_seconds}"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(bitrate_kbps),
            },
            {"key": "FFmpegMetadata", "add_metadata": True},
        ],
    }
    try:
        with (factory or _default_factory)(opts) as ydl:
            ydl.extract_info(canonical_url(info.video_id), download=True)
    except yt_dlp.utils.DownloadError as exc:
        log.warning("convert failed for %s: %s", info.video_id, exc)
        raise ConvertError("The convert failed. Try again later.") from exc

    path = out_dir / f"{info.video_id}.mp3"
    if not path.is_file():
        raise ConvertError("The convert failed. Try again later.")
    return ConvertResult(info=info, path=path, filename=mp3_filename(info.title, info.video_id))
