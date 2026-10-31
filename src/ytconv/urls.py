"""Turn a pasted link into a canonical single-video URL, or refuse it.

Runs before any network call, so a bad link never reaches yt-dlp (SSRF guard).
"""

import re
from urllib.parse import parse_qs, urlsplit

ALLOWED_HOSTS = frozenset(
    {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"}
)
# Path prefixes that carry the video id as the next segment.
_ID_PATHS = ("shorts", "embed", "live")
_VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}")
_MAX_URL_LENGTH = 2048


class InvalidUrlError(ValueError):
    """The link is not a single YouTube video we accept."""


def parse_video_id(raw: str) -> str:
    """Return the 11-character video id from a YouTube link."""
    url = raw.strip()
    if not url or len(url) > _MAX_URL_LENGTH:
        raise InvalidUrlError("Paste a YouTube video link.")
    if "://" not in url:
        # Postel: people often paste "youtu.be/..." without the scheme.
        url = f"https://{url}"

    parts = urlsplit(url)
    if parts.scheme != "https":
        raise InvalidUrlError("Only https links are accepted.")
    if parts.username or parts.password or parts.port:
        raise InvalidUrlError("Paste a YouTube video link.")
    host = (parts.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise InvalidUrlError("Only YouTube links are accepted.")

    segments = [s for s in parts.path.split("/") if s]
    candidate: str | None = None
    if host == "youtu.be":
        candidate = segments[0] if segments else None
    elif segments[:1] == ["watch"]:
        values = parse_qs(parts.query).get("v", [])
        candidate = values[0] if values else None
    elif len(segments) >= 2 and segments[0] in _ID_PATHS:
        candidate = segments[1]
    elif segments[:1] == ["playlist"]:
        raise InvalidUrlError("Playlists aren't supported. Paste a single video link.")

    if candidate is None or not _VIDEO_ID.fullmatch(candidate):
        raise InvalidUrlError("That link doesn't point to a single video.")
    return candidate


def canonical_url(video_id: str) -> str:
    if not _VIDEO_ID.fullmatch(video_id):
        raise InvalidUrlError("That link doesn't point to a single video.")
    return f"https://www.youtube.com/watch?v={video_id}"
