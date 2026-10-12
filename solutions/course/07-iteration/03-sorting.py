
def alpha(words: list[str]) -> list[str]:
    return sorted(words)


def shortest_first(words: list[str]) -> list[str]:
    return sorted(words, key=len)


def by_last_letter(words: list[str]) -> list[str]:
    return sorted(words, key=lambda word: word[-1])
