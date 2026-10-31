from fastapi.testclient import TestClient

from ytconv import __version__
from ytconv.main import app

client = TestClient(app)


def test_healthz_reports_ok_and_version() -> None:
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "version": __version__}


def test_api_docs_are_not_exposed() -> None:
    assert client.get("/docs").status_code == 404
