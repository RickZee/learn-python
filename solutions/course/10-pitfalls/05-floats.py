from decimal import Decimal


def money(cents: str, extra: str) -> str:
    return str(Decimal(cents) + Decimal(extra))


def total(cents: str, extra: str) -> str:
    left = Decimal(cents)
    right = Decimal(extra)
    summed = left + right
    return str(summed)


def same_money(left: str, right: str) -> bool:
    return Decimal(left) == Decimal(right)


def nearly_third(total: float) -> bool:
    return abs(total - 0.3) < 1e-9
