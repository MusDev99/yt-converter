# Changelog

## 2026-10-31 04:43 · v0.1.0

- feat: project scaffold (Python 3.13, FastAPI, uv, `/healthz`), settings from `YTCONV_*` env vars
- build: Dockerfile with ffmpeg, non-root user; `compose.yaml` bound to 127.0.0.1
- ci: `verify` (ruff + mypy --strict + pytest + pip-audit), `docker` (build + health smoke) and `branch-policy` workflows, PR template, weekly Dependabot
- docs: CLAUDE.md (private scope rules), README, feature spec, shared code-review skill
