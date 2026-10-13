from pathlib import Path

import pytest
from readinglist.import_csv import CsvImportError, import_csv
from readinglist.store import BookStore


def test_import_adds_rows(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    path = tmp_path / "books.csv"
    path.write_text("isbn,title\n9781,Alpha\n9782,\n", encoding="utf-8")
    added, skipped = import_csv(store, path)
    assert added == 2
    assert skipped == 0
    assert len(store.list()) == 2


def test_import_skips_duplicates_and_missing_file(tmp_path: Path):
    store = BookStore(tmp_path / "books.db")
    store.add("9781", title="Alpha")
    path = tmp_path / "books.csv"
    path.write_text("isbn,title\n9781,Again\n9782,Beta\n", encoding="utf-8")
    added, skipped = import_csv(store, path)
    assert added == 1
    assert skipped == 1
    with pytest.raises(CsvImportError):
        import_csv(store, tmp_path / "missing.csv")
