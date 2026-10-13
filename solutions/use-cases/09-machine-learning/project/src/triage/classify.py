from __future__ import annotations

import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel


class Ticket(BaseModel):
    text: str
    label: str


class Client(Protocol):
    def classify(self, text: str) -> str: ...


def classify_all(client: Client, texts: list[str]) -> list[Ticket]:
    return [Ticket(text=text, label=client.classify(text)) for text in texts]


def accuracy(got: list[Ticket], expected: list[str]) -> float:
    if not expected:
        return 1.0
    hits = sum(ticket.label == label for ticket, label in zip(got, expected, strict=True))
    return hits / len(expected)


def confusion_matrix(
    got: list[Ticket], expected: list[str], labels: list[str]
) -> dict[str, dict[str, int]]:
    matrix = {row: {col: 0 for col in labels} for row in labels}
    for ticket, want in zip(got, expected, strict=True):
        if want in matrix and ticket.label in matrix[want]:
            matrix[want][ticket.label] += 1
    return matrix


def precision_recall(matrix: dict[str, dict[str, int]], label: str) -> tuple[float, float]:
    true_positive = matrix[label][label]
    predicted = sum(matrix[row][label] for row in matrix)
    actual = sum(matrix[label].values())
    precision = true_positive / predicted if predicted else 0.0
    recall = true_positive / actual if actual else 0.0
    return precision, recall


def classify_all_retry(client: Client, texts: list[str], failures_allowed: int = 2) -> list[Ticket]:
    tickets: list[Ticket] = []
    for text in texts:
        label = "unknown"
        for attempt in range(failures_allowed + 1):
            try:
                label = client.classify(text)
                break
            except TimeoutError:
                time.sleep(0.01 * (attempt + 1))
        tickets.append(Ticket(text=text, label=label))
    return tickets


def classify_all_bounded(client: Client, texts: list[str], workers: int = 2) -> list[Ticket]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        labels = list(pool.map(client.classify, texts))
    return [Ticket(text=text, label=label) for text, label in zip(texts, labels, strict=True)]


def classify_cached(client: Client, texts: list[str], cache_dir: Path) -> list[Ticket]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    tickets: list[Ticket] = []
    for text in texts:
        key = hashlib.sha256(text.encode("utf-8")).hexdigest()
        path = cache_dir / key
        if path.exists():
            label = path.read_text(encoding="utf-8")
        else:
            label = client.classify(text)
            path.write_text(label, encoding="utf-8")
        tickets.append(Ticket(text=text, label=label))
    return tickets
