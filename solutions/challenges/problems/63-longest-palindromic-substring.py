def longest_palindrome(s: str) -> str:
    """Longest palindromic substring (any longest if ties).

    Approach: expand around 2n-1 centers (odd and even length).
    Time: O(n²)
    Space: O(1)
    Alternative: DP table P[i][j]; Manacher's algorithm O(n).
    Common bugs: only expanding odd centers; wrong inclusive end after expand.
    """
    if not s:
        return ""
    start = end = 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for i in range(len(s)):
        left, right = expand(i, i)
        if right - left > end - start:
            start, end = left, right
        left, right = expand(i, i + 1)
        if right - left > end - start:
            start, end = left, right
    return s[start : end + 1]
