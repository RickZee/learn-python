from pathlib import Path

import httpx
from readinglist.enrich import enrich_missing
from readinglist.store import BookStore


class Lookup:
    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping

    def get_title(self, isbn: str) -> str | None:
        return self.mapping.get(isbn)


def test_enrich_fills_blank_titles(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    store.add("9781")
    store.add("9782", title="Keep")
    updated = enrich_missing(store, Lookup({"9781": "Alpha", "9782": "Nope"}))
    assert updated == 1
    assert store.get(1)["title"] == "Alpha"
    assert store.get(2)["title"] == "Keep"


def test_enrich_with_httpx_mock(tmp_path: Path):
    from readinglist.enrich import HttpxTitleClient

    store = BookStore(tmp_path / "books.db")
    store.add("9781")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"title": "From API"})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        lookup = HttpxTitleClient(client, "https://example.test/books")
        assert enrich_missing(store, lookup) == 1
    assert store.get(1)["title"] == "From API"
