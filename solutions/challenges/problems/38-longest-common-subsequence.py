
def longest_common_subsequence(text1: str, text2: str) -> int:
    """Length of the longest common subsequence.

    Approach: one row of the classic table.
    Time: O(len(text1) * len(text2))
    Space: O(len(text2))
    Alternative: the full two-dimensional table.
    Common bugs: using a substring, which must be contiguous.
    """
    previous = [0] * (len(text2) + 1)
    for i in range(1, len(text1) + 1):
        current = [0] * (len(text2) + 1)
        for j in range(1, len(text2) + 1):
            if text1[i - 1] == text2[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]
