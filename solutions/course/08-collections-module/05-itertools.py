
import functools
import itertools


def first_counts(n: int) -> list[int]:
    return list(itertools.islice(itertools.count(0), n))


def opening(n: int) -> list[int]:
    return list(itertools.islice(itertools.count(0), n))


def fib(n: int) -> int:
    def raw(value: int) -> int:
        if value < 2:
            return value
        return raw(value - 1) + raw(value - 2)

    cached = functools.cache(raw)
    return cached(n)
