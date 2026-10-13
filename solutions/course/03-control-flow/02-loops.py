def count_char(text: str, target: str) -> int:
    count = 0
    for char in text:
        if char == target:
            count += 1
    return count


def sum_to(n: int) -> int:
    total = 0
    for value in range(1, n + 1):
        total = total + value
    return total


def vowels_or_none(text: str) -> str:
    found = ""
    for char in text:
        if char in "aeiou":
            found = found + char
    if found == "":
        return "none"
    return found


def aisle_seats(n: int) -> int:
    count = 0
    for value in range(1, n + 1):
        if value % 2 == 0:
            count += 1
    return count
