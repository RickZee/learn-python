from __future__ import annotations

from pathlib import Path
from typing import Protocol

from fastapi import FastAPI


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


def create_app(database: Path | None = None, store: Store | None = None) -> FastAPI:
    raise NotImplementedError
