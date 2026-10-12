def same_value(a, b) -> bool:
    return a == b


def same_object(a, b) -> bool:
    return a is b


def both_missing(a, b) -> bool:
    return a is None and b is None
