from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from readinglist.store import BookStore


def create_app(database: Path | None = None, store: BookStore | None = None) -> FastAPI:
    raise NotImplementedError
