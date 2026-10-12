from collections import Counter


def count_of(items: list[str], value: str) -> int:
    return Counter(items)[value]


def top_item(items: list[str]) -> str:
    return Counter(items).most_common(1)[0][0]


def winning_tally(votes: list[str]) -> int:
    return Counter(votes).most_common(1)[0][1]
