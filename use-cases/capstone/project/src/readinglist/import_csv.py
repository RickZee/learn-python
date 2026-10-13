from __future__ import annotations

from pathlib import Path

from readinglist.store import BookStore


class CsvImportError(Exception):
    """Raised when the CSV file cannot be read."""


def import_csv(store: BookStore, path: Path) -> tuple[int, int]:
    """Import isbn,title rows. Return (added, skipped)."""
    raise NotImplementedError
