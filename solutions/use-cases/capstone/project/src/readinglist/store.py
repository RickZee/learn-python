from __future__ import annotations

import sqlite3
from pathlib import Path

ALLOWED_STATUS = frozenset({"read", "unread", "reading"})


class DuplicateIsbnError(Exception):
    """Raised when a book with this ISBN already exists."""


class InvalidStatusError(Exception):
    """Raised when status is not read/unread/reading."""


class BookStore:
    def __init__(self, database: Path) -> None:
        database.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            create table if not exists books (
                id integer primary key,
                isbn text not null unique,
                title text,
                status text not null default 'unread'
            )
            """
        )
        self.connection.commit()

    def add(self, isbn: str, title: str | None = None, status: str = "unread") -> dict:
        status = status or "unread"
        if status not in ALLOWED_STATUS:
            raise InvalidStatusError(f"invalid status '{status}'")
        try:
            cursor = self.connection.execute(
                "insert into books (isbn, title, status) values (?, ?, ?)",
                (isbn, title, status),
            )
            self.connection.commit()
        except sqlite3.IntegrityError as exc:
            raise DuplicateIsbnError(f"duplicate isbn '{isbn}'") from exc
        return self.get(int(cursor.lastrowid))  # type: ignore[arg-type]

    def list(self, status: str | None = None) -> list[dict]:
        if status is not None and status not in ALLOWED_STATUS:
            raise InvalidStatusError(f"invalid status '{status}'")
        if status is None:
            rows = self.connection.execute(
                "select id, isbn, title, status from books order by id"
            ).fetchall()
        else:
            rows = self.connection.execute(
                "select id, isbn, title, status from books where status = ? order by id",
                (status,),
            ).fetchall()
        return [self._row(row) for row in rows]

    def get(self, book_id: int) -> dict | None:
        row = self.connection.execute(
            "select id, isbn, title, status from books where id = ?",
            (book_id,),
        ).fetchone()
        return None if row is None else self._row(row)

    def set_title(self, book_id: int, title: str) -> dict | None:
        cursor = self.connection.execute(
            "update books set title = ? where id = ?",
            (title, book_id),
        )
        self.connection.commit()
        if cursor.rowcount == 0:
            return None
        return self.get(book_id)

    def set_status(self, book_id: int, status: str) -> dict | None:
        if status not in ALLOWED_STATUS:
            raise InvalidStatusError(f"invalid status '{status}'")
        cursor = self.connection.execute(
            "update books set status = ? where id = ?",
            (status, book_id),
        )
        self.connection.commit()
        if cursor.rowcount == 0:
            return None
        return self.get(book_id)

    @staticmethod
    def _row(row: sqlite3.Row) -> dict:
        return {
            "id": row["id"],
            "isbn": row["isbn"],
            "title": row["title"],
            "status": row["status"],
        }
