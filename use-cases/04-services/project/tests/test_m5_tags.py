from fastapi.testclient import TestClient
from notes_api.app import MemoryStore, create_app


def test_create_with_tags():
    client = TestClient(create_app(store=MemoryStore()))
    created = client.post("/notes", json={"title": "a", "body": "b", "tags": ["work"]})
    assert created.json()["tags"] == ["work"]


def test_filter_by_tag():
    client = TestClient(create_app(store=MemoryStore()))
    client.post("/notes", json={"title": "a", "body": "b", "tags": ["work"]})
    client.post("/notes", json={"title": "c", "body": "d", "tags": ["home"]})
    assert [n["title"] for n in client.get("/notes", params={"tag": "work"}).json()] == ["a"]
