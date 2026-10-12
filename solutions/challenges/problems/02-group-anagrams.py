def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that use the same letters. Group order does not matter.

    Approach: the sorted letters are the key in a map of lists.
    Time: O(n * k log k), where k is the word length
    Space: O(n * k)
    Alternative: count the 26 letters and use that count as the key.
    Common bugs: sorting the word you use as the key and losing the original.
    """
    from collections import defaultdict

    groups = defaultdict(list)
    for word in words:
        groups[tuple(sorted(word))].append(word)
    return list(groups.values())
