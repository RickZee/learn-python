def alpha(words: list[str]) -> list[str]:
    return sorted(words)


def shortest_first(words: list[str]) -> list[str]:
    primary = sorted(words)
    by_len = sorted(primary, key=len)
    result = list(by_len)
    return result


def by_score_then_name(rows: list[tuple[str, int]]) -> list[tuple[str, int]]:
    by_name = sorted(rows, key=lambda row: row[0])
    by_score = sorted(by_name, key=lambda row: row[1])
    result = list(by_score)
    return result


def by_last_letter(words: list[str]) -> list[str]:
    return sorted(words, key=lambda word: word[-1])
