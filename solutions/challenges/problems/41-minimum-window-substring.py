def min_window(s: str, t: str) -> str:
    """Shortest substring of s that covers every character of t.

    Approach: grow a window until it covers t, then shrink it.
    Time: O(len(s) + len(t))
    Space: O(alphabet)
    Alternative: check every substring.
    Common bugs: treating two copies of the same letter in t as one.
    """
    from collections import Counter

    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    best = ""
    left = 0
    for right, character in enumerate(s):
        if need[character] > 0:
            missing -= 1
        need[character] -= 1
        while missing == 0:
            window = s[left : right + 1]
            if best == "" or len(window) < len(best):
                best = window
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return best
