from collections import Counter


def count_of(items: list[str], value: str) -> int:
    counts = Counter(items)
    total = counts[value]
    return total


def top_item(items: list[str]) -> str:
    counts = Counter(items)
    ranked = counts.most_common(1)
    winner = ranked[0][0]
    return winner


def winning_tally(votes: list[str]) -> int:
    return Counter(votes).most_common(1)[0][1]
