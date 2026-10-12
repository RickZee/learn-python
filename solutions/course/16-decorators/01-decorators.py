
import functools


def add_one(func):
    def wrapper(n: int) -> int:
        return func(n) + 1

    return wrapper


def shout(func):
    @functools.wraps(func)
    def wrapper(text: str) -> str:
        return func(text).upper()

    return wrapper


def plain(name: str) -> str:
    return name


def in_dollars(func):
    @functools.wraps(func)
    def wrapper() -> float:
        return func() / 100

    return wrapper


def price_cents() -> int:
    return 250
