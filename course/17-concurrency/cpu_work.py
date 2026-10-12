"""Picklable CPU helpers for process-pool demos."""


def square(value: int) -> int:
    return value * value


def busy(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total
