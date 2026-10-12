from typing import Any, Protocol, TypedDict, runtime_checkable


def first[T](items: list[T]) -> T:
    if not items:
        raise ValueError("empty")
    return items[0]


@runtime_checkable
class SizedName(Protocol):
    name: str


def has_name(obj: Any) -> bool:
    return isinstance(obj, SizedName)


class Book(TypedDict):
    title: str
    pages: int


def shout_title(row: Book) -> str:
    return row["title"].upper()
