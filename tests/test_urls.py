import pytest

from ytconv.urls import InvalidUrlError, canonical_url, parse_video_id

VID = "dQw4w9WgXcQ"


@pytest.mark.parametrize(
    "url",
    [
        f"https://www.youtube.com/watch?v={VID}",
        f"https://youtube.com/watch?v={VID}&t=42s",
        f"https://m.youtube.com/watch?v={VID}",
        f"https://music.youtube.com/watch?v={VID}&si=abc",
        f"https://youtu.be/{VID}",
        f"https://youtu.be/{VID}?si=share",
        f"https://www.youtube.com/shorts/{VID}",
        f"https://www.youtube.com/embed/{VID}",
        f"https://www.youtube.com/live/{VID}",
        f"youtu.be/{VID}",
        f"  https://WWW.YouTube.com/watch?v={VID}  ",
        # A video inside a playlist: take the video, ignore the list.
        f"https://www.youtube.com/watch?v={VID}&list=PL123",
    ],
)
def test_accepts_single_video_links(url: str) -> None:
    assert parse_video_id(url) == VID


@pytest.mark.parametrize(
    ("url", "reason"),
    [
        ("", "Paste"),
        (f"http://www.youtube.com/watch?v={VID}", "https"),
        (f"https://evil.com/watch?v={VID}", "Only YouTube"),
        (f"https://youtube.com.evil.com/watch?v={VID}", "Only YouTube"),
        (f"https://user:pw@youtube.com/watch?v={VID}", "Paste"),
        (f"https://youtube.com:8443/watch?v={VID}", "Paste"),
        ("https://www.youtube.com/playlist?list=PL123", "Playlists"),
        ("https://www.youtube.com/@somechannel", "single video"),
        ("https://www.youtube.com/watch?v=short", "single video"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ;rm", "single video"),
        ("file:///etc/passwd", "https"),
        ("https://" + "a" * 3000, "Paste"),
    ],
)
def test_rejects_everything_else(url: str, reason: str) -> None:
    with pytest.raises(InvalidUrlError, match=reason):
        parse_video_id(url)


def test_canonical_url() -> None:
    assert canonical_url(VID) == f"https://www.youtube.com/watch?v={VID}"
    with pytest.raises(InvalidUrlError):
        canonical_url("../../etc")
