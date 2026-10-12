
import functools


def shout(func):
    @functools.wraps(func)
    def wrapper(text: str) -> str:
        return func(text).upper()

    return wrapper
