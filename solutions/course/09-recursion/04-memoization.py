import functools


def cached_hits(n: int) -> int:
    def grow(current: int) -> int:
        if current >= 10:
            return current
        return grow(current * 2)

    grow = functools.cache(grow)
    grow(n)
    grow(n)
    return grow.cache_info().hits


def min_steps(n: int) -> int:
    def best(current: int) -> int:
        if current <= 1:
            return 0
        if current % 2 == 0:
            return 1 + min(best(current - 1), best(current // 2))
        return 1 + best(current - 1)

    best = functools.cache(best)
    return best(n)


def choose_table(n: int, k: int) -> int:
    seen: dict[tuple[int, int], int] = {}

    def choose(a: int, b: int) -> int:
        if b == 0 or b == a:
            return 1
        key = (a, b)
        if key in seen:
            return seen[key]
        seen[key] = choose(a - 1, b - 1) + choose(a - 1, b)
        return seen[key]

    return choose(n, k)


def choose_hits(n: int, k: int) -> int:
    calls = {"n": 0}

    def choose(a: int, b: int) -> int:
        calls["n"] += 1
        if b == 0 or b == a:
            return 1
        return choose(a - 1, b - 1) + choose(a - 1, b)

    choose = functools.cache(choose)
    choose(n, k)
    return calls["n"]
