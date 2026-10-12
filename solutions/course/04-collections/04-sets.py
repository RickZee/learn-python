def has(seen: set[int], value: int) -> bool:
    return value in seen


def in_both(a: list[int], b: list[int]) -> set[int]:
    return set(a) & set(b)


def missing_rsvp(invited: list[int], rsvped: list[int]) -> set[int]:
    return set(invited) - set(rsvped)
