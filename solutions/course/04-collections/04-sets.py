def has(seen: set[int], value: int) -> bool:
    return value in seen


def missing_rsvp(invited: list[int], rsvped: list[int]) -> set[int]:
    invited_set = set(invited)
    rsvped_set = set(rsvped)
    missing = invited_set - rsvped_set
    return missing


def unique_pairs(points: list[list[int]]) -> set:
    pairs = set()
    for point in points:
        pairs.add(tuple(point))
    return pairs


def in_both(a: list[int], b: list[int]) -> set[int]:
    return set(a) & set(b)
