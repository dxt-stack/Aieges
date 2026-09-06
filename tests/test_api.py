from fastapi.testclient import TestClient

from aegis.api import app

client = TestClient(app)


def test_dashboard_and_status_are_available():
    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert "AEGIS" in dashboard.text

    status = client.get("/api/status")
    assert status.status_code == 200
    assert status.json()["name"] == "AEGIS"


def test_private_research_targets_are_rejected():
    response = client.post("/api/research/audit-url", json={"url": "http://127.0.0.1:8000"})
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]
