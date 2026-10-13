def seen_index(nums: list[int], value: int) -> int:
    seen = {item: index for index, item in enumerate(nums)}
    return seen.get(value, -1)


def first_index(nums: list[int], value: int) -> int:
    for index, item in enumerate(nums):
        if item == value:
            return index
    return -1


def first_unique(text: str) -> int:
    """Return the index of the first character that appears once, or -1.

    Approach: count, then walk the text once.
    Time: O(n)
    Space: O(1) for a fixed alphabet, O(n) in general
    Alternative: a dict of first indexes, then a second pass.
    Common bugs: returning the character instead of the index.
    """
    from collections import Counter

    counts = Counter(text)
    for index, character in enumerate(text):
        if counts[character] == 1:
            return index
    return -1
