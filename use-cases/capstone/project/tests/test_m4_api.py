from pathlib import Path

from fastapi.testclient import TestClient
from readinglist.api import create_app
from readinglist.store import BookStore


def test_create_list_read(tmp_path: Path):
    client = TestClient(create_app(store=BookStore(tmp_path / "books.db")))
    created = client.post("/books", json={"isbn": "9781", "title": "Alpha"})
    assert created.status_code == 201
    assert created.json()["title"] == "Alpha"
    assert client.get("/books").json()[0]["isbn"] == "9781"
    assert client.get("/books/1").json()["id"] == 1


def test_missing_and_duplicate(tmp_path: Path):
    client = TestClient(create_app(store=BookStore(tmp_path / "books.db")))
    assert client.get("/books/9").status_code == 404
    client.post("/books", json={"isbn": "9781"})
    assert client.post("/books", json={"isbn": "9781"}).status_code == 409
