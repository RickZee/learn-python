def multiplier(n: int):
    def mul(x: int) -> int:
        return x * n

    return mul


def adder(n: int):
    def add(x: int, captured=n) -> int:
        total = x + captured
        return total

    return add


def make_handlers(labels: list[str]):
    handlers = []
    for label in labels:

        def handler(label: str = label) -> str:
            return label

        handlers.append(handler)
    return handlers


def subtractor(n: int):
    def sub(x: int) -> int:
        return x - n

    return sub
