# CLAUDE.md

yt-converter: a **private, personal** tool. Paste a YouTube link, get an MP3 to download. Python 3.13 + FastAPI + yt-dlp + ffmpeg in one Docker image, run locally first (Cloud Run optional later). Process and standards: [Agentic Coding Style](https://musdev99.github.io/agentic-coding-style) and [BRANCHING.md](https://github.com/MusDev99/agentic-coding-style/blob/main/BRANCHING.md). Plan: https://claude.ai/artifact/KTfFF2vJUSGvGnNgMfCqoZ

## Scope (decided 2026-10-31, do not widen)

- Only the owner can use it (sign-in allowlist from Week 3). **Never** add a public mode, open sign-up or sharing links.
- For content the user owns or that is Creative Commons / public domain. The UI asks the user to confirm rights before every convert.
- No playlists, no channel downloads, no video output. Max length `YTCONV_MAX_DURATION_SECONDS` (15 min), rate limited, files deleted after `YTCONV_RETENTION_SECONDS` (1 h). No history of URLs is kept.

## Commands

```bash
uv sync            # install (Python 3.13, uv)
make run           # dev server on http://127.0.0.1:8000
make verify        # ruff + format check + mypy --strict + pytest (= CI, run before every commit)
make docker        # docker compose up --build (bound to 127.0.0.1 only)
```

## Architecture

- `src/ytconv/main.py`: FastAPI app. `/healthz` only for now; convert routes arrive in Week 2.
- `src/ytconv/config.py`: all limits and paths come from `YTCONV_*` env vars via `get_settings()`. No magic numbers elsewhere. Document new variables in `.env.example`.
- Pure logic (URL validation, filenames, limits) goes in its own modules with unit tests in `tests/`. Network calls to YouTube are mocked in tests; never hit YouTube from CI.
- `Dockerfile`: one image for local and Cloud Run, ffmpeg from Debian, non-root user, `PORT` env. `compose.yaml` binds to `127.0.0.1` only.

## Rules

- Strict typing: `mypy --strict` clean, no `Any` without a reason, no `# type: ignore` without a comment.
- **Never build a shell command from user input.** Call yt-dlp through its Python API and ffmpeg with an argument list (`subprocess.run([...])`, never `shell=True`).
- Accept only `youtube.com`, `www.youtube.com`, `m.youtube.com`, `music.youtube.com` and `youtu.be` URLs over https; reject everything else before any network call (SSRF).
- Pin exact versions in `pyproject.toml`; commit `uv.lock`. yt-dlp breaks often, Dependabot bumps it weekly.
- Secrets only in env; never commit `.env*`.
- User-facing errors are short and generic; details go to the server log. Never log tokens or cookies.
- Frontend (Week 2): mobile-first at 375px, touch targets ≥ 44px, respect `prefers-reduced-motion`, apply the [Laws of UX](https://lawsofux.com/) and name the law in the PR.

## Git

Never commit to `main`. Branches `feat/` `fix/` `chore/` `docs/` (agent sessions may use their given `claude/` branch). Conventional Commits for commits and PR titles (checked by `branch-policy.yml`). Squash merge, one concern per PR, under ~400 changed lines (`uv.lock` doesn't count). CI `verify`, `docker` and `branch-policy` must be green. Run the code-review skill (`.agents/skills/code-review/SKILL.md`) before every PR. Update README + CHANGELOG in the same PR. SemVer tags `vX.Y.Z`.
