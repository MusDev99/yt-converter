"""Command line: `python -m ytconv <link> --confirm-rights [--out DIR]`.

Week 1 way to try the converter before the web app lands.
"""

import argparse
import shutil
import sys
from pathlib import Path

from ytconv.config import get_settings
from ytconv.converter import ConvertError, check_duration, convert, probe
from ytconv.urls import InvalidUrlError, parse_video_id

RIGHTS_NOTICE = (
    "Only convert videos you own or that are Creative Commons / public domain.\n"
    "Re-run with --confirm-rights to confirm you have the rights to this audio."
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ytconv", description="YouTube link to MP3 (private use)."
    )
    parser.add_argument("url", help="YouTube video link")
    parser.add_argument(
        "--confirm-rights",
        action="store_true",
        help="I own this content or it is Creative Commons / public domain",
    )
    parser.add_argument("--out", type=Path, default=Path.cwd(), help="folder for the MP3")
    args = parser.parse_args(argv)

    if not args.confirm_rights:
        print(RIGHTS_NOTICE, file=sys.stderr)
        return 2
    if shutil.which("ffmpeg") is None:
        print("ffmpeg isn't installed. Install it, or use `make docker`.", file=sys.stderr)
        return 1

    settings = get_settings()
    try:
        video_id = parse_video_id(args.url)
        info = probe(video_id)
        check_duration(info, settings.max_duration_seconds)
        licence = "Creative Commons" if info.is_creative_commons else (info.license or "standard")
        mins, secs = divmod(info.duration_seconds, 60)
        print(f"🎵 {info.title} · {info.uploader} · {mins}:{secs:02d} · licence: {licence}")
        result = convert(
            info,
            settings.download_dir / video_id,
            bitrate_kbps=settings.audio_bitrate_kbps,
            max_seconds=settings.max_duration_seconds,
        )
    except (InvalidUrlError, ConvertError) as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / result.filename
    shutil.move(result.path, target)
    print(f"✅ Saved {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
