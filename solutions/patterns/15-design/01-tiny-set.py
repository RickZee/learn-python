def evicted(keys: list[int], capacity: int) -> int | None:
    from collections import OrderedDict

    data: OrderedDict[int, bool] = OrderedDict()
    dropped = None
    for key in keys:
        data[key] = True
        if len(data) > capacity:
            dropped, _ = data.popitem(last=False)
    return dropped


class TinySet:
    """A set of ints with add, remove, and contains.

    Approach: a Python set.
    Time: O(1) average for each call
    Space: O(n)
    Alternative: a dict of keys.
    Common bugs: remove raising when the key is missing.
    """

    def __init__(self) -> None:
        self.data: set[int] = set()

    def add(self, key: int) -> None:
        self.data.add(key)

    def remove(self, key: int) -> None:
        self.data.discard(key)

    def contains(self, key: int) -> bool:
        return key in self.data


def survived() -> bool:
    box = TinySet()
    box.add(1)
    box.remove(1)
    return box.contains(1)


def refreshed() -> bool:
    box = TinySet()
    box.add(1)
    return box.contains(1)
