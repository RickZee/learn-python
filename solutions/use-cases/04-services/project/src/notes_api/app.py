import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class NoteIn(BaseModel):
    title: str
    body: str


def create_app(database: Path) -> FastAPI:
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database, check_same_thread=False)
    connection.execute(
        "create table if not exists notes (id integer primary key, title text, body text)"
    )
    app = FastAPI()

    @app.post("/notes", status_code=201)
    def create_note(note: NoteIn) -> dict:
        cursor = connection.execute(
            "insert into notes (title, body) values (?, ?)", (note.title, note.body)
        )
        connection.commit()
        return {"id": cursor.lastrowid, "title": note.title, "body": note.body}

    @app.get("/notes")
    def list_notes() -> list[dict]:
        rows = connection.execute("select id, title, body from notes order by id").fetchall()
        return [{"id": row[0], "title": row[1], "body": row[2]} for row in rows]

    @app.get("/notes/{note_id}")
    def read_note(note_id: int) -> dict:
        row = connection.execute(
            "select id, title, body from notes where id = ?", (note_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404)
        return {"id": row[0], "title": row[1], "body": row[2]}

    return app
