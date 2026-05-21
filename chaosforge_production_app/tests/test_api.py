from fastapi.testclient import TestClient
from chaosforge.api.app import app

client = TestClient(app)

def test_dashboard_loads():
    r = client.get("/")
    assert r.status_code == 200
    assert "ChaosForge" in r.text
