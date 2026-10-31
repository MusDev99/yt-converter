from pathlib import Path
from typing import Any

import pytest

from tests.fakes import Recorder
from ytconv.converter import ConvertError, VideoInfo, check_duration, convert, probe

VID = "dQw4w9WgXcQ"
RAW: dict[str, Any] = {
    "id": VID,
    "title": "My Track",
    "uploader": "Me",
    "duration": 185,
    "license": "Creative Commons Attribution license (reuse allowed)",
}


def info(**overrides: Any) -> VideoInfo:
    base: dict[str, Any] = {
        "video_id": VID,
        "title": "My Track",
        "uploader": "Me",
        "duration_seconds": 185,
        "license": None,
    }
    return VideoInfo(**(base | overrides))


def test_probe_reads_metadata_without_downloading() -> None:
    rec = Recorder(RAW)
    got = probe(VID, factory=rec)
    assert got == info(license=RAW["license"])
    assert got.is_creative_commons
    ydl = rec.built[0]
    assert ydl.calls == [(f"https://www.youtube.com/watch?v={VID}", False)]
    assert ydl.opts["noplaylist"] is True


@pytest.mark.parametrize(
    ("raw", "reason"),
    [
        (RAW | {"is_live": True}, "Live"),
        (RAW | {"live_status": "is_upcoming"}, "Live"),
        (RAW | {"duration": None}, "length"),
    ],
)
def test_probe_rejects_unconvertible(raw: dict[str, Any], reason: str) -> None:
    with pytest.raises(ConvertError, match=reason):
        probe(VID, factory=Recorder(raw))


def test_probe_hides_yt_dlp_details() -> None:
    with pytest.raises(ConvertError, match="private") as exc:
        probe(VID, factory=Recorder(RAW, error="ERROR: secret internal detail"))
    assert "secret" not in str(exc.value)


def test_standard_licence_is_not_cc() -> None:
    assert not info(license=None).is_creative_commons
    assert not info(license="Standard YouTube License").is_creative_commons


def test_check_duration() -> None:
    check_duration(info(duration_seconds=900), 900)
    with pytest.raises(ConvertError, match="15-minute"):
        check_duration(info(duration_seconds=901), 900)


def test_convert_writes_mp3_and_suggests_name(tmp_path: Path) -> None:
    rec = Recorder(RAW)
    result = convert(info(), tmp_path / "out", bitrate_kbps=192, max_seconds=900, factory=rec)
    assert result.path == tmp_path / "out" / f"{VID}.mp3"
    assert result.path.read_bytes() == b"ID3fake"
    assert result.filename == "My Track.mp3"

    opts = rec.built[0].opts
    assert opts["outtmpl"].endswith("%(id)s.%(ext)s")
    assert opts["noplaylist"] is True
    extract = opts["postprocessors"][0]
    assert extract == {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }
    # Second length guard inside yt-dlp: rejects long videos, passes short ones.
    assert opts["match_filter"]({"duration": 1000}, incomplete=False) is not None
    assert opts["match_filter"]({"duration": 100}, incomplete=False) is None


def test_convert_refuses_long_video_before_download(tmp_path: Path) -> None:
    rec = Recorder(RAW)
    with pytest.raises(ConvertError, match="limit"):
        convert(
            info(duration_seconds=3600), tmp_path, bitrate_kbps=192, max_seconds=900, factory=rec
        )
    assert rec.built == []


def test_convert_failure_is_generic(tmp_path: Path) -> None:
    with pytest.raises(ConvertError, match="Try again later"):
        convert(
            info(),
            tmp_path,
            bitrate_kbps=192,
            max_seconds=900,
            factory=Recorder(RAW, error="HTTP Error 403"),
        )


def test_convert_missing_output_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(ConvertError):
        convert(
            info(),
            tmp_path,
            bitrate_kbps=192,
            max_seconds=900,
            factory=Recorder(RAW, write_mp3=False),
        )
