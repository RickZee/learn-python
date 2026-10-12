
def multiplier(n: int):
    def mul(x: int) -> int:
        return x * n

    return mul


def adder(n: int):
    def add(x: int) -> int:
        return x + n

    return add


def subtractor(n: int):
    def sub(x: int) -> int:
        return x - n

    return sub
