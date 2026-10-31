"""Fake yt-dlp downloader so tests never reach YouTube."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yt_dlp


class FakeYDL:
    def __init__(
        self,
        opts: Mapping[str, Any],
        info: Mapping[str, Any],
        *,
        error: str | None = None,
        write_mp3: bool = True,
    ) -> None:
        self.opts = opts
        self.info = info
        self.error = error
        self.write_mp3 = write_mp3
        self.calls: list[tuple[str, bool]] = []

    def __enter__(self) -> "FakeYDL":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def extract_info(self, url: str, download: bool = True) -> Any:
        self.calls.append((url, download))
        if self.error:
            raise yt_dlp.utils.DownloadError(self.error)
        if download and self.write_mp3:
            out = Path(
                str(self.opts["outtmpl"]).replace("%(id)s.%(ext)s", f"{self.info['id']}.mp3")
            )
            out.write_bytes(b"ID3fake")
        return dict(self.info)


class Recorder:
    """Factory that remembers every FakeYDL it builds."""

    def __init__(self, info: Mapping[str, Any], **kwargs: Any) -> None:
        self.info = info
        self.kwargs = kwargs
        self.built: list[FakeYDL] = []

    def __call__(self, opts: Mapping[str, Any]) -> FakeYDL:
        ydl = FakeYDL(opts, self.info, **self.kwargs)
        self.built.append(ydl)
        return ydl
