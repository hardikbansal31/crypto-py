from fastapi.testclient import TestClient
from mcp_server.server import app

client = TestClient(app)


def test_ping():
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
