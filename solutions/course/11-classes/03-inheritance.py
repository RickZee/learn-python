def extra(n: int) -> int:
    return n + 1


class Counter:
    def __init__(self) -> None:
        self.value = 0

    def add(self, n: int) -> int:
        self.value += n
        return self.value


class Step(Counter):
    def add(self, n: int) -> int:
        return super().add(n + 1)


def bumped() -> int:
    return Step().add(1)


def two_steps() -> int:
    step = Step()
    first = step.add(1)
    second = step.add(1)
    return second
