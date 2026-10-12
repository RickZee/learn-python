
from decimal import Decimal


def money(cents: str, extra: str) -> str:
    return str(Decimal(cents) + Decimal(extra))


def total(cents: str, extra: str) -> str:
    return str(Decimal(cents) + Decimal(extra))


def same_money(left: str, right: str) -> bool:
    return Decimal(left) == Decimal(right)
