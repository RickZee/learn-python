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


def double(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) * 2

    return wrapper


def stamped(name: str) -> str:
    decorated = shout(plain)
    text = decorated(name)
    result = str(text)
    return result
