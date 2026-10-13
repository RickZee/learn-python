from fastapi.testclient import TestClient
from notes_api.app import MemoryStore, create_app


def test_search_q():
    client = TestClient(create_app(store=MemoryStore()))
    client.post("/notes", json={"title": "alpha", "body": "one"})
    client.post("/notes", json={"title": "beta", "body": "two"})
    assert [n["title"] for n in client.get("/notes", params={"q": "alp"}).json()] == ["alpha"]


def test_limit_offset():
    client = TestClient(create_app(store=MemoryStore()))
    for name in "abcd":
        client.post("/notes", json={"title": name, "body": name})
    page = client.get("/notes", params={"limit": 2, "offset": 1}).json()
    assert [n["title"] for n in page] == ["b", "c"]
