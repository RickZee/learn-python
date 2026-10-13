def append_one(lst: list[int] | None = None) -> list[int]:
    if lst is None:
        lst = []
    lst.append(1)
    return lst


def append_item(item: int, lst: list[int] | None = None) -> list[int]:
    if lst is None:
        lst = []
    lst.append(item)
    return lst


def broken_append(lst=None):
    if lst is None:
        lst = []
    lst.append(1)
    return lst
