from fastapi.testclient import TestClient
from notes_api.app import MemoryStore, create_app


def test_empty_title_422():
    client = TestClient(create_app(store=MemoryStore()))
    assert client.post("/notes", json={"title": "", "body": "b"}).status_code == 422


def test_long_title_422():
    client = TestClient(create_app(store=MemoryStore()))
    assert client.post("/notes", json={"title": "x" * 101, "body": "b"}).status_code == 422
