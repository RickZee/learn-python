def by_length(words: list[str]) -> dict[int, str]:
    return {len(word): word for word in words}


def lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}


def tag_lengths(tags: list[str]) -> set[int]:
    return {len(tag) for tag in tags}
