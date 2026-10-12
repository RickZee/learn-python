from collections import defaultdict


def key_of(word: str):
    return tuple(sorted(word))


def by_length(words: list[str]) -> dict[int, list[str]]:
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)

def is_anagram(left: str, right: str) -> bool:
    """True when both strings use the same characters the same number of times.

    Approach: compare character counts.
    Time: O(n)
    Space: O(1) for a fixed alphabet
    Alternative: sort both strings and compare.
    Common bugs: comparing lengths only.
    """
    from collections import Counter

    return Counter(left) == Counter(right)
