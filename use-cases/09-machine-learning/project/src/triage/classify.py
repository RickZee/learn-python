from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pydantic import BaseModel


class Ticket(BaseModel):
    text: str
    label: str


class Client(Protocol):
    def classify(self, text: str) -> str: ...


def classify_all(client: Client, texts: list[str]) -> list[Ticket]:
    raise NotImplementedError


def accuracy(got: list[Ticket], expected: list[str]) -> float:
    raise NotImplementedError


def confusion_matrix(
    got: list[Ticket], expected: list[str], labels: list[str]
) -> dict[str, dict[str, int]]:
    raise NotImplementedError


def precision_recall(matrix: dict[str, dict[str, int]], label: str) -> tuple[float, float]:
    raise NotImplementedError


def classify_all_retry(client: Client, texts: list[str], failures_allowed: int = 2) -> list[Ticket]:
    raise NotImplementedError


def classify_all_bounded(client: Client, texts: list[str], workers: int = 2) -> list[Ticket]:
    raise NotImplementedError


def classify_cached(client: Client, texts: list[str], cache_dir: Path) -> list[Ticket]:
    raise NotImplementedError
