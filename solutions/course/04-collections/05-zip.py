def indexes(items: list[str]) -> list[tuple[int, str]]:
    return list(enumerate(items))


def numbered(lines: list[str]) -> list[str]:
    labeled = []
    for number, line in enumerate(lines, start=1):
        labeled.append(f"{number}. {line}")
    return labeled


def pair_up(left: list[int], right: list[str]) -> list[tuple[int, str]]:
    return list(zip(left, right))


def pair_strict(left: list[int], right: list[str]) -> list[tuple[int, str]]:
    return list(zip(left, right, strict=True))
