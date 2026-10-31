"""HTTP entry point. Week 0: health check only; convert routes land in Week 2."""

from fastapi import FastAPI

from ytconv import __version__

app = FastAPI(title="yt-converter", version=__version__, docs_url=None, redoc_url=None)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
