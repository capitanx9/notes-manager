from fastapi.testclient import TestClient

from src.notes_manager.main import app

client = TestClient(app)


def test_liveness():
    response = client.get("/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
