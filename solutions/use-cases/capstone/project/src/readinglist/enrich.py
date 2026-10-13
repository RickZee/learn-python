from __future__ import annotations

from typing import Protocol

import httpx

from readinglist.store import BookStore


class TitleClient(Protocol):
    def get_title(self, isbn: str) -> str | None: ...


class HttpxTitleClient:
    """Look up a title at ``{base_url}/{isbn}`` expecting JSON ``{"title": "..."}``."""

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        self.client = client
        self.base_url = base_url.rstrip("/")

    def get_title(self, isbn: str) -> str | None:
        response = self.client.get(f"{self.base_url}/{isbn}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        payload = response.json()
        title = payload.get("title")
        return title if title else None


def enrich_missing(store: BookStore, client: TitleClient) -> int:
    """Fill blank titles via ``client.get_title(isbn)``. Return how many updated."""
    updated = 0
    for book in store.list():
        if book["title"]:
            continue
        title = client.get_title(book["isbn"])
        if title:
            store.set_title(book["id"], title)
            updated += 1
    return updated
