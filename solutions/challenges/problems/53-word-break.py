def word_break(s: str, words: list[str]) -> bool:
    """Whether s is a concatenation of dictionary words (reuse allowed).

    Approach: ok[i] means s[:i] segments; try every prior break j.
    Time: O(n² * L) with string slices
    Space: O(n)
    Alternative: memoized recursion from each index; trie of words.
    Common bugs: forbidding reuse; checking only whole-prefix membership.
    """
    wordset = set(words)
    ok = [False] * (len(s) + 1)
    ok[0] = True
    for i in range(1, len(s) + 1):
        ok[i] = any(ok[j] and s[j:i] in wordset for j in range(i))
    return ok[-1]
