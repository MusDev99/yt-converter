# Feature: core convert (Week 1)

## 🎯 Goal
Turn one YouTube video link into an MP3 file, safely, with the private-scope limits built in. Reused unchanged by the Week 2 web API.

## ✅ Acceptance
| # | Check | How |
|---|---|---|
| 1 | Only https single-video links on YouTube hosts are accepted; playlists, channels, other hosts, credentials/ports refused before any network call | `tests/test_urls.py` |
| 2 | Metadata (title, uploader, length, licence) read without downloading; CC licence flagged | `test_probe_*` |
| 3 | Live/upcoming streams and videos over `YTCONV_MAX_DURATION_SECONDS` refused before download, and again inside yt-dlp | `test_probe_rejects_unconvertible`, `test_convert_refuses_long_video_before_download`, `match_filter` assertion |
| 4 | Output is `<id>.mp3` at the configured bitrate with title/artist tags; download name is a safe `Title.mp3` | `test_convert_writes_mp3_and_suggests_name`, `tests/test_naming.py`, manual ffprobe check |
| 5 | Users never see yt-dlp internals | `test_probe_hides_yt_dlp_details`, `test_convert_failure_is_generic` |
| 6 | CLI refuses without `--confirm-rights` | `tests/test_cli.py` |

## ⚠️ Risks
- YouTube blocks data-centre IPs and changes often; Dependabot bumps yt-dlp weekly, local Docker is the default runtime.
- A video with no length reported is refused (stricter than needed, safe).

## 🔒 Security
SSRF: host allowlist + id regex, URL rebuilt from the id. No shell: yt-dlp Python API only. Path traversal: files named by id; titles only used for the suggested name after stripping `/ \ : * ? " < > |` and control characters.

## 🧠 Laws of UX
CLI only this week. Postel's Law: links without `https://`, with tracking params, mixed case or surrounding spaces are accepted. Clear error messages say what to do next.
