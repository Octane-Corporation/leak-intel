import json
from fastapi.testclient import TestClient
from leakintel.api.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_search_returns_list():
    # Make sure data is loaded
    client.post("/ingest")
    r = client.get("/search")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
