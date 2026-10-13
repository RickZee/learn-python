def leftover(n: int, size: int) -> int:
    return n % size


def split_bill(subtotal: int, tip_percent: int, people: int) -> int:
    tip = subtotal * tip_percent // 100
    total = subtotal + tip
    share = total // people
    return share


def change(cents: int) -> tuple[int, int]:
    return divmod(cents, 100)
