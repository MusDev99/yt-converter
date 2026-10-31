# Changelog

## 2026-10-31 07:06 · v0.2.0

- feat(urls): accept only single-video YouTube links (https, host allowlist, no playlists), checked before any network call
- feat(converter): yt-dlp + ffmpeg to MP3 (`YTCONV_AUDIO_BITRATE_KBPS`, default 192) with title/artist tags; live streams and videos over the length limit refused before download; licence read so Creative Commons videos are flagged
- feat(cli): `ytconv <link> --confirm-rights --out DIR`
- test: 48 new tests with a fake downloader (no YouTube in CI)
## 2026-10-31 15:15

- ci: `branch-cleanup.yml` deletes a PR's branch after it is merged (skips forks, `main`, stacked bases)

## 2026-10-31 04:43 · v0.1.0

- feat: project scaffold (Python 3.13, FastAPI, uv, `/healthz`), settings from `YTCONV_*` env vars
- build: Dockerfile with ffmpeg, non-root user; `compose.yaml` bound to 127.0.0.1
- ci: `verify` (ruff + mypy --strict + pytest + pip-audit), `docker` (build + health smoke) and `branch-policy` workflows, PR template, weekly Dependabot
- docs: CLAUDE.md (private scope rules), README, feature spec, shared code-review skill
