
def adder_at(n: int):
    def add(x: int, n: int = n) -> int:
        return x + n

    return add


def plus(n: int):
    def add(x: int, n: int = n) -> int:
        return x + n

    return add


def times(n: int):
    def mul(x: int, n: int = n) -> int:
        return x * n

    return mul
