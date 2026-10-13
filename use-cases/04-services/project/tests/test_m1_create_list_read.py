from fastapi.testclient import TestClient
from notes_api.app import MemoryStore, create_app


def test_create_list_read():
    client = TestClient(create_app(store=MemoryStore()))
    created = client.post("/notes", json={"title": "a", "body": "b"})
    assert created.status_code == 201
    assert created.json()["title"] == "a"
    assert client.get("/notes").json()[0]["body"] == "b"
    assert client.get("/notes/1").json()["id"] == 1


def test_missing_is_404():
    client = TestClient(create_app(store=MemoryStore()))
    assert client.get("/notes/9").status_code == 404
