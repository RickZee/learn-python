def min_distance(word1: str, word2: str) -> int:
    """Minimum insert/delete/replace edits to turn word1 into word2.

    Approach: classic DP compressed to one row with a saved diagonal.
    Time: O(m * n)
    Space: O(n)
    Alternative: full 2D table; recursion with cache.
    Common bugs: losing the diagonal when rolling one row; wrong empty init.
    """
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            cur = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = cur
    return dp[n]
