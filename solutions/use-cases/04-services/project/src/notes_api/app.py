from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Protocol

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str
    tags: list[str] = Field(default_factory=list)


class Store(Protocol):
    def create(self, title: str, body: str, tags: list[str] | None = None) -> dict: ...
    def list(
        self,
        q: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        tag: str | None = None,
    ) -> list[dict]: ...
    def get(self, note_id: int) -> dict | None: ...
    def update(self, note_id: int, title: str, body: str) -> dict | None: ...
    def delete(self, note_id: int) -> bool: ...


class MemoryStore:
    def __init__(self) -> None:
        self._notes: dict[int, dict] = {}
        self._next = 1

    def create(self, title: str, body: str, tags: list[str] | None = None) -> dict:
        note = {"id": self._next, "title": title, "body": body, "tags": list(tags or [])}
        self._notes[self._next] = note
        self._next += 1
        return note

    def list(
        self,
        q: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        tag: str | None = None,
    ) -> list[dict]:
        items = list(self._notes.values())
        if q:
            items = [
                n
                for n in items
                if q.lower() in n["title"].lower() or q.lower() in n["body"].lower()
            ]
        if tag:
            items = [n for n in items if tag in n.get("tags", [])]
        items = items[offset:]
        if limit is not None:
            items = items[:limit]
        return items

    def get(self, note_id: int) -> dict | None:
        return self._notes.get(note_id)

    def update(self, note_id: int, title: str, body: str) -> dict | None:
        note = self._notes.get(note_id)
        if note is None:
            return None
        note["title"] = title
        note["body"] = body
        return note

    def delete(self, note_id: int) -> bool:
        return self._notes.pop(note_id, None) is not None


class SqliteStore:
    def __init__(self, database: Path) -> None:
        database.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.connection.execute(
            "create table if not exists notes (id integer primary key, title text, body text, tags text)"
        )

    def create(self, title: str, body: str, tags: list[str] | None = None) -> dict:
        tags = tags or []
        cursor = self.connection.execute(
            "insert into notes (title, body, tags) values (?, ?, ?)",
            (title, body, ",".join(tags)),
        )
        self.connection.commit()
        return {"id": cursor.lastrowid, "title": title, "body": body, "tags": tags}

    def list(
        self,
        q: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        tag: str | None = None,
    ) -> list[dict]:
        rows = self.connection.execute(
            "select id, title, body, tags from notes order by id"
        ).fetchall()
        items = [
            {
                "id": row[0],
                "title": row[1],
                "body": row[2],
                "tags": [t for t in row[3].split(",") if t],
            }
            for row in rows
        ]
        return _filter(items, q, limit, offset, tag)

    def get(self, note_id: int) -> dict | None:
        row = self.connection.execute(
            "select id, title, body, tags from notes where id = ?", (note_id,)
        ).fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "title": row[1],
            "body": row[2],
            "tags": [t for t in row[3].split(",") if t],
        }

    def update(self, note_id: int, title: str, body: str) -> dict | None:
        note = self.get(note_id)
        if note is None:
            return None
        self.connection.execute(
            "update notes set title = ?, body = ? where id = ?", (title, body, note_id)
        )
        self.connection.commit()
        note["title"] = title
        note["body"] = body
        return note

    def delete(self, note_id: int) -> bool:
        cursor = self.connection.execute("delete from notes where id = ?", (note_id,))
        self.connection.commit()
        return cursor.rowcount > 0


def _filter(items, q, limit, offset, tag):
    if q:
        items = [
            n for n in items if q.lower() in n["title"].lower() or q.lower() in n["body"].lower()
        ]
    if tag:
        items = [n for n in items if tag in n.get("tags", [])]
    items = items[offset:]
    if limit is not None:
        items = items[:limit]
    return items


def create_app(database: Path | None = None, store: Store | None = None) -> FastAPI:
    backend: Store = store or SqliteStore(database or Path("notes.db"))
    app = FastAPI()

    @app.post("/notes", status_code=201)
    def create_note(note: NoteIn) -> dict:
        return backend.create(note.title, note.body, note.tags)

    @app.get("/notes")
    def list_notes(
        q: str | None = None,
        limit: int | None = Query(default=None, ge=1),
        offset: int = Query(default=0, ge=0),
        tag: str | None = None,
    ) -> list[dict]:
        return backend.list(q=q, limit=limit, offset=offset, tag=tag)

    @app.get("/notes/{note_id}")
    def read_note(note_id: int) -> dict:
        note = backend.get(note_id)
        if note is None:
            raise HTTPException(status_code=404)
        return note

    @app.put("/notes/{note_id}")
    def update_note(note_id: int, note: NoteIn) -> dict:
        updated = backend.update(note_id, note.title, note.body)
        if updated is None:
            raise HTTPException(status_code=404)
        return updated

    @app.delete("/notes/{note_id}", status_code=204)
    def delete_note(note_id: int) -> None:
        if not backend.delete(note_id):
            raise HTTPException(status_code=404)

    return app
