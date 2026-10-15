def evens(numbers: list[int]) -> list[int]:
    return [n for n in numbers if n % 2 == 0]


def drop_all(items: list, bad) -> list:
    kept = []
    for item in items:
        if item != bad:
            kept.append(item)
    return kept


def strip_blanks(lines: list[str]) -> list[str]:
    return [line for line in lines if line != ""]


def positions(items: list, target) -> list[int]:
    found = []
    for index, item in enumerate(items):
        if item == target:
            found.append(index)
    return found
