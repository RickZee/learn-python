from pathlib import Path

from fastapi.testclient import TestClient
from readinglist.api import create_app
from readinglist.cli import app
from readinglist.store import BookStore
from typer.testing import CliRunner

runner = CliRunner()


def test_store_and_filter_status(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    first = store.add("9781", title="Alpha")
    store.add("9782", title="Beta")
    store.set_status(first["id"], "read")
    assert [book["isbn"] for book in store.list(status="read")] == ["9781"]
    assert [book["isbn"] for book in store.list(status="unread")] == ["9782"]


def test_cli_and_api_mark(tmp_path: Path):
    database = tmp_path / "books.db"
    store = BookStore(database)
    store.add("9781", title="Alpha")
    marked = runner.invoke(app, ["mark", "1", "read", "--database", str(database)])
    assert marked.exit_code == 0
    assert "read" in marked.stdout
    client = TestClient(create_app(store=BookStore(database)))
    response = client.patch("/books/1/status", json={"status": "reading"})
    assert response.status_code == 200
    assert response.json()["status"] == "reading"
    bad = client.patch("/books/1/status", json={"status": "nope"})
    assert bad.status_code == 422
