from __future__ import annotations

from readinglist.store import BookStore


def enrich_missing(store: BookStore, client) -> int:
    """Fill blank titles via client.get_title(isbn). Return how many updated."""
    raise NotImplementedError
