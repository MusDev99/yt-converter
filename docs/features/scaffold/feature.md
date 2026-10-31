# Feature: project scaffold (Week 0)

## 🎯 Goal
A repo that follows agentic-coding-style from the first PR, so Week 1 can start on convert logic straight away.

## ✅ Acceptance
| # | Check | How |
|---|---|---|
| 1 | `make verify` green (ruff, format, mypy --strict, pytest) | CI `verify` |
| 2 | Docker image builds with ffmpeg and answers `/healthz` | CI `docker` |
| 3 | Branch name + PR title enforced | CI `branch-policy` |
| 4 | Private scope written down for future agents | `CLAUDE.md` → Scope |
| 5 | Dependencies pinned, lockfile committed, weekly updates | `pyproject.toml`, `uv.lock`, `dependabot.yml` |

## ⚠️ Risks
- YouTube blocks data-centre IPs, so Cloud Run may fail; local Docker is the default.
- yt-dlp breaks when YouTube changes; weekly Dependabot bump.

## 🔒 Security
No user input yet. `/docs` and `/redoc` disabled. Container runs as non-root with a read-only root filesystem in compose.

## 🧠 Laws of UX
None yet (no UI). Applied from Week 2.
