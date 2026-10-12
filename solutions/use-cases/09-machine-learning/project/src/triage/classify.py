from typing import Protocol

from pydantic import BaseModel


class Ticket(BaseModel):
    text: str
    label: str


class Client(Protocol):
    def classify(self, text: str) -> str: ...


def classify_all(client: Client, texts: list[str]) -> list[Ticket]:
    tickets = []
    for text in texts:
        label = ""
        for _ in range(2):
            try:
                label = client.classify(text)
                break
            except TimeoutError:
                continue
        tickets.append(Ticket(text=text, label=label))
    return tickets


def accuracy(got: list[Ticket], expected: list[str]) -> float:
    if not expected:
        return 1.0
    hits = sum(ticket.label == label for ticket, label in zip(got, expected, strict=True))
    return hits / len(expected)
