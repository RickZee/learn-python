def character_replacement(s: str, k: int) -> int:
    """Longest substring equalized with at most k replacements.

    Approach: window valid while len - max_freq <= k; expand right, shrink left.
    Time: O(n)
    Space: O(alphabet)
    Alternative: check every substring's counts.
    Common bugs: budgeting distinct characters instead of replacements.
    """
    from collections import defaultdict

    counts = defaultdict(int)
    left = best = max_count = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        max_count = max(max_count, counts[ch])
        while right - left + 1 - max_count > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
