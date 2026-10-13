def adder_at(n: int):
    def add(x: int, n: int = n) -> int:
        return x + n

    return add


def plus(n: int):
    def add(x: int, n: int = n) -> int:
        total = x + n
        return total

    return add


def times(n: int):
    def mul(x: int, n: int = n) -> int:
        return x * n

    return mul


def make_handlers(limit: int) -> list:
    handlers = []
    for n in range(limit):
        handlers.append(lambda n=n: n)
    return handlers
