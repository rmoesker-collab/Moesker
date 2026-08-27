from fastapi.testclient import TestClient
from typer.testing import CliRunner

from stahltrace import __version__
from stahltrace.cli import app as cli_app
from stahltrace.server import app as server_app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(cli_app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_health_endpoint() -> None:
    client = TestClient(server_app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__
