def first(pair: tuple[int, int]) -> int:
    return pair[0]


def swap(pair: tuple[int, int]) -> tuple[int, int]:
    left, right = pair
    first_out = right
    second_out = left
    return (first_out, second_out)


def bump_left(pair: tuple[int, int]) -> tuple[int, int]:
    left, right = pair
    updated = (left + 1, right)
    return updated


def panel_mid(scores: tuple[int, int, int]) -> int:
    return scores[1]
