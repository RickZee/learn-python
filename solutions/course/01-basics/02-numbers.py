def leftover(n: int, size: int) -> int:
    return n % size


def groups_of(n: int, size: int) -> tuple[int, int]:
    return divmod(n, size)


def change(cents: int) -> tuple[int, int]:
    return divmod(cents, 100)
