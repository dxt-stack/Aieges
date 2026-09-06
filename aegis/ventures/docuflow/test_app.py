import pytest
from fastapi.testclient import TestClient
from .app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_process_task():
    payload = {"payload": {"invoice_number": "INV-2026-901", "total": 1450.00}}
    response = client.post("/v1/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert "task_id" in data
