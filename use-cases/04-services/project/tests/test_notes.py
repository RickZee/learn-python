from fastapi.testclient import TestClient
from notes_api.app import create_app


def test_create_list_and_read(tmp_path):
    client = TestClient(create_app(tmp_path / "notes.db"))
    created = client.post("/notes", json={"title": "a", "body": "b"})
    assert created.status_code == 201
    assert created.json()["title"] == "a"
    listed = client.get("/notes")
    assert listed.json() == [{"id": 1, "title": "a", "body": "b"}]
    one = client.get("/notes/1")
    assert one.json()["body"] == "b"
    missing = client.get("/notes/9")
    assert missing.status_code == 404
