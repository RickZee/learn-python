def by_length(words: list[str]) -> dict[int, str]:
    return {len(word): word for word in words}


def lengths(words: list[str]) -> dict[str, int]:
    mapping = {}
    for word in words:
        mapping[word] = len(word)
    return mapping


def two_passes(words: list[str]) -> tuple[int, int]:
    values = tuple(len(w) for w in words)
    first = sum(values)
    second = sum(values)
    return first, second


def tag_lengths(tags: list[str]) -> set[int]:
    return {len(tag) for tag in tags}
