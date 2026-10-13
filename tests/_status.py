"""Pending paths for round-5 guards, listed in docs/maintainers/status.md."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "maintainers" / "status.md"
_HEADING = re.compile(r"^##\s+(G\d+)\b")
_BULLET = re.compile(r"^-\s+(\S+)\s*$")


def pending(guard: str) -> set[str]:
    """Return paths listed under ``## G<n> ...`` in status.md."""
    if not STATUS.is_file():
        return set()
    paths: set[str] = set()
    current: str | None = None
    for line in STATUS.read_text(encoding="utf-8").splitlines():
        heading = _HEADING.match(line)
        if heading:
            current = heading.group(1)
            continue
        if current != guard:
            continue
        bullet = _BULLET.match(line.strip())
        if bullet:
            paths.add(bullet.group(1))
    return paths
