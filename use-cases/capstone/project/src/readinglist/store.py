from __future__ import annotations

from pathlib import Path


class DuplicateIsbnError(Exception):
    """Raised when a book with this ISBN already exists."""


class BookStore:
    def __init__(self, database: Path) -> None:
        raise NotImplementedError

    def add(self, isbn: str, title: str | None = None, status: str = "unread") -> dict:
        raise NotImplementedError

    def list(self, status: str | None = None) -> list[dict]:
        raise NotImplementedError

    def get(self, book_id: int) -> dict | None:
        raise NotImplementedError

    def set_title(self, book_id: int, title: str) -> dict | None:
        raise NotImplementedError

    def set_status(self, book_id: int, status: str) -> dict | None:
        raise NotImplementedError
