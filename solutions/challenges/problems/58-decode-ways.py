def num_decodings(s: str) -> int:
    """Count ways to decode a digit string with A=1 … Z=26.

    Approach: rolling DP—add one-digit and valid two-digit transitions.
    Time: O(n)
    Space: O(1)
    Alternative: dp array of size n+1; memoized recursion.
    Common bugs: treating '0' as a solo digit; accepting 05 as five.
    """
    if not s or s[0] == "0":
        return 0
    prev2, prev1 = 1, 1
    for i in range(1, len(s)):
        cur = 0
        if s[i] != "0":
            cur += prev1
        two = int(s[i - 1 : i + 1])
        if 10 <= two <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
