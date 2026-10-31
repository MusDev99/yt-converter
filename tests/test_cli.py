from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

import ytconv.__main__ as cli
from tests.fakes import Recorder
from ytconv import converter
from ytconv.config import get_settings

VID = "dQw4w9WgXcQ"
RAW: dict[str, Any] = {"id": VID, "title": "My Track", "uploader": "Me", "duration": 65}


@pytest.fixture
def fake_youtube(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[Recorder]:
    rec = Recorder(RAW)
    monkeypatch.setattr(converter, "_default_factory", rec)
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/ffmpeg")
    monkeypatch.setenv("YTCONV_DOWNLOAD_DIR", str(tmp_path / "work"))
    get_settings.cache_clear()
    yield rec
    get_settings.cache_clear()


def test_requires_rights_confirmation(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main([f"https://youtu.be/{VID}"]) == 2
    assert "--confirm-rights" in capsys.readouterr().err


def test_converts_and_saves(
    fake_youtube: Recorder, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "music"
    assert cli.main([f"https://youtu.be/{VID}", "--confirm-rights", "--out", str(out)]) == 0
    assert (out / "My Track.mp3").read_bytes() == b"ID3fake"
    printed = capsys.readouterr().out
    assert "1:05" in printed
    assert "Saved" in printed


def test_bad_link_never_reaches_youtube(
    fake_youtube: Recorder, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["https://evil.com/x", "--confirm-rights"]) == 1
    assert fake_youtube.built == []
    assert "Only YouTube" in capsys.readouterr().err


def test_missing_ffmpeg(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("shutil.which", lambda _: None)
    assert cli.main([f"https://youtu.be/{VID}", "--confirm-rights"]) == 1
    assert "ffmpeg" in capsys.readouterr().err
