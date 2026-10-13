from pathlib import Path

import pytest
from readinglist.store import BookStore, DuplicateIsbnError


def test_add_and_list(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    book = store.add("9780000000001", title="Alpha")
    assert book["isbn"] == "9780000000001"
    assert book["title"] == "Alpha"
    assert store.list() == [book]


def test_duplicate_isbn_raises(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    store.add("9780000000001")
    with pytest.raises(DuplicateIsbnError):
        store.add("9780000000001")


def test_get_missing_is_none(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    assert store.get(99) is None
