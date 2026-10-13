"""Shared text helpers for guard tests."""

from __future__ import annotations

import re


def normalize(text: str) -> str:
    """Lowercase, treat - and _ as spaces, collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"[-_]", " ", text.casefold())).strip()
