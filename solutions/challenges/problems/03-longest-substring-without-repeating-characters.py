def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring with no repeated character.

    Approach: a window remembers the last index of each character.
    Time: O(n)
    Space: O(k) for the characters in the window
    Alternative: grow the window and shrink it with a set until it is unique.
    Common bugs: moving the window start backward, or keeping a repeated character.
    """
    last = {}
    start = 0
    best = 0
    for index, character in enumerate(s):
        if character in last and last[character] >= start:
            start = last[character] + 1
        last[character] = index
        best = max(best, index - start + 1)
    return best
