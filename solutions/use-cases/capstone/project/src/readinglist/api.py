from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from readinglist.store import ALLOWED_STATUS, BookStore, DuplicateIsbnError, InvalidStatusError


class BookIn(BaseModel):
    isbn: str = Field(min_length=1)
    title: str | None = None
    status: str = "unread"


class StatusIn(BaseModel):
    status: str


def create_app(database: Path | None = None, store: BookStore | None = None) -> FastAPI:
    backend = store or BookStore(database or Path("readinglist.db"))
    app = FastAPI()

    @app.post("/books", status_code=201)
    def create_book(book: BookIn) -> dict:
        try:
            return backend.add(book.isbn, title=book.title, status=book.status)
        except DuplicateIsbnError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except InvalidStatusError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/books")
    def list_books(status: str | None = Query(default=None)) -> list[dict]:
        try:
            return backend.list(status=status)
        except InvalidStatusError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/books/{book_id}")
    def read_book(book_id: int) -> dict:
        book = backend.get(book_id)
        if book is None:
            raise HTTPException(status_code=404)
        return book

    @app.patch("/books/{book_id}/status")
    def mark_status(book_id: int, body: StatusIn) -> dict:
        if body.status not in ALLOWED_STATUS:
            raise HTTPException(status_code=422, detail=f"invalid status '{body.status}'")
        book = backend.set_status(book_id, body.status)
        if book is None:
            raise HTTPException(status_code=404)
        return book

    return app
