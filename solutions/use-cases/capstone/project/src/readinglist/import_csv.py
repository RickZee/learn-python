from __future__ import annotations

import csv
from pathlib import Path

from readinglist.store import BookStore, DuplicateIsbnError


class CsvImportError(Exception):
    """Raised when the CSV file cannot be read."""


def import_csv(store: BookStore, path: Path) -> tuple[int, int]:
    """Import isbn,title rows. Return (added, skipped)."""
    if not path.exists():
        raise CsvImportError(f"missing file '{path}'")
    added = 0
    skipped = 0
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "isbn" not in reader.fieldnames:
            raise CsvImportError("CSV must have an isbn column")
        for index, row in enumerate(reader, start=2):
            isbn = (row.get("isbn") or "").strip()
            if not isbn:
                raise CsvImportError(f"ragged or empty isbn on line {index}")
            title = (row.get("title") or "").strip() or None
            try:
                store.add(isbn, title=title)
                added += 1
            except DuplicateIsbnError:
                skipped += 1
    return added, skipped
