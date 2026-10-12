
class Count:
    def __init__(self, n: int) -> None:
        self.n = n

    def __len__(self) -> int:
        return self.n


def size(n: int) -> int:
    return len(Count(n))


class Bag:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __getitem__(self, index: int) -> str:
        return self.items[index]


def at(items: list[str], index: int) -> str:
    return Bag(items)[index]


class Pocket:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __contains__(self, item: object) -> bool:
        return item in self.items


def holds(items: list[str], item: str) -> bool:
    return item in Pocket(items)
