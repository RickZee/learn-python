from fastapi.testclient import TestClient
from notes_api.app import MemoryStore, create_app


def test_update_and_delete():
    client = TestClient(create_app(store=MemoryStore()))
    client.post("/notes", json={"title": "a", "body": "b"})
    updated = client.put("/notes/1", json={"title": "c", "body": "d"})
    assert updated.status_code == 200
    assert updated.json()["title"] == "c"
    assert client.delete("/notes/1").status_code == 204
    assert client.get("/notes/1").status_code == 404


def test_update_missing_404():
    client = TestClient(create_app(store=MemoryStore()))
    assert client.put("/notes/1", json={"title": "c", "body": "d"}).status_code == 404
