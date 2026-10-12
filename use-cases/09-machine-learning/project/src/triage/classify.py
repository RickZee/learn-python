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
