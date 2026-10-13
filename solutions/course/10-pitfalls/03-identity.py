def same_value(a, b) -> bool:
    return a == b


def same_object(a, b) -> bool:
    left = a
    right = b
    match = left is right
    return match


def both_missing(a, b) -> bool:
    return a is None and b is None


def is_zero(total: int) -> bool:
    return total == 0
