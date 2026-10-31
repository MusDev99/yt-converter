# 🎵 yt-converter

Private, personal tool: paste a YouTube link, get an MP3 to download.

> ⚠️ **For content you own or that is Creative Commons / public domain only.** Downloading other YouTube content breaches YouTube's Terms of Service and can infringe copyright. This app is built to run privately for one person and must never be hosted as a public service.

## ✨ Features

| Status | Feature |
|---|---|
| ✅ | Project scaffold, CI, Docker image with ffmpeg, `/healthz` |
| 🔜 Week 1 | URL validation, yt-dlp + ffmpeg to MP3 (192 kbps) with ID3 tags |
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

Settings live in `.env` (copy `.env.example`).

## 🗂️ Structure

```
src/ytconv/     app code (main.py = FastAPI, config.py = settings)
tests/          pytest
docs/features/  feature specs
.agents/skills/ shared code-review checklist
```

## 🧭 Standards

[Agentic Coding Style](https://musdev99.github.io/agentic-coding-style) · [BRANCHING.md](https://github.com/MusDev99/agentic-coding-style/blob/main/BRANCHING.md) · rules for agents in [CLAUDE.md](CLAUDE.md) · history in [CHANGELOG.md](CHANGELOG.md).

🧹 `branch-cleanup.yml` deletes the branch once its PR is merged (keep *Automatically delete head branches* on too).
