import pytest

from ytconv.naming import mp3_filename


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("My Song", "My Song.mp3"),
        ("AC/DC: Live?  ", "AC DC Live.mp3"),
        ("../../etc/passwd", "etc passwd.mp3"),
        ("tab\tand\nnewline", "tab and newline.mp3"),
        ("...", "abc123.mp3"),
        ("", "abc123.mp3"),
        ("Lagu Raya 🎶", "Lagu Raya 🎶.mp3"),
    ],
)
def test_mp3_filename(title: str, expected: str) -> None:
    assert mp3_filename(title, "abc123") == expected


def test_long_titles_are_capped() -> None:
    assert len(mp3_filename("x" * 500, "id")) == 100 + len(".mp3")
