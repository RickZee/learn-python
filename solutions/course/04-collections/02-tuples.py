def first(pair: tuple[int, int]) -> int:
    return pair[0]


def swap(pair: tuple[int, int]) -> tuple[int, int]:
    left, right = pair
    return (right, left)


def panel_mid(scores: tuple[int, int, int]) -> int:
    return scores[1]
