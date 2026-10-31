"""Safe download file names from video titles."""

import re
import unicodedata

_UNSAFE = re.compile(r'[\\/:*?"<>|\x00-\x1f]+')
_SPACES = re.compile(r"\s+")
_MAX_STEM = 100


def mp3_filename(title: str, fallback: str) -> str:
    """`Song Title.mp3`, stripped of path and control characters, never empty."""
    stem = unicodedata.normalize("NFC", title)
    stem = _UNSAFE.sub(" ", stem)
    stem = _SPACES.sub(" ", stem).strip(" .")[:_MAX_STEM].rstrip(" .")
    return f"{stem or fallback}.mp3"
