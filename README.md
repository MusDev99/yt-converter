# 🎵 yt-converter

Private, personal tool: paste a YouTube link, get an MP3 to download.

> ⚠️ **For content you own or that is Creative Commons / public domain only.** Downloading other YouTube content breaches YouTube's Terms of Service and can infringe copyright. This app is built to run privately for one person and must never be hosted as a public service.

## ✨ Features

| Status | Feature |
|---|---|
| ✅ | Project scaffold, CI, Docker image with ffmpeg, `/healthz` |
| ✅ Week 1 | URL validation, yt-dlp + ffmpeg to MP3 (192 kbps) with title/artist tags, 15-min limit, CLI |
| 🔜 Week 2 | Job API with progress + mobile web app (paste, preview, convert, download) |
| 🔜 Week 3 | Google sign-in allowlist, rate limits, rights confirmation, auto-delete |
| 🔜 Week 4 | v1.0.0: local Docker (+ Tailscale for phone), optional Cloud Run |

## 🚀 Run it

```bash
uv sync
make run        # http://127.0.0.1:8000/healthz
make verify     # lint + typecheck + tests
make docker     # same app in Docker, on 127.0.0.1:8000
```

### 🎧 Convert from the command line (Week 1)

Needs [ffmpeg](https://ffmpeg.org/download.html) (`brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install ffmpeg`).

```bash
uv run ytconv "https://youtu.be/<id>" --confirm-rights --out ~/Music
# 🎵 My Track · Me · 3:05 · licence: Creative Commons
# ✅ Saved /Users/you/Music/My Track.mp3
```

`--confirm-rights` is required: only convert videos you own or that are Creative Commons / public domain. The licence YouTube reports is printed so you can check.

Settings live in `.env` (copy `.env.example`): max length, MP3 bitrate (128/192/256/320), work folder.

## 🗂️ Structure

```
src/ytconv/     app code: urls.py (link check), converter.py (yt-dlp + ffmpeg),
                naming.py, __main__.py (CLI), main.py (FastAPI), config.py
tests/          pytest
docs/features/  feature specs
.agents/skills/ shared code-review checklist
```

## 🧭 Standards

[Agentic Coding Style](https://musdev99.github.io/agentic-coding-style) · [BRANCHING.md](https://github.com/MusDev99/agentic-coding-style/blob/main/BRANCHING.md) · rules for agents in [CLAUDE.md](CLAUDE.md) · history in [CHANGELOG.md](CHANGELOG.md).

🧹 `branch-cleanup.yml` deletes the branch once its PR is merged (keep *Automatically delete head branches* on too).
