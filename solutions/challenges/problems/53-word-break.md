# 53. Word Break — walkthrough

## Recognize it
Can you concatenate dictionary words (reuse allowed) to rebuild string `s` exactly? Look-alike: word break II (return all sentences). Another look-alike: word search on a board (paths, not concatenation).

## Brute force
At each index, try every word that matches the prefix and recurse. Without memo, overlapping suffixes are re-solved exponentially—`aaaa…` with word `"a"` is the classic blow-up.

## Key insight
`ok[i]` means `s[:i]` can be segmented. `ok[0] = True`. For each end `i`, set `ok[i]` if some `j < i` has `ok[j]` and `s[j:i]` is in the dictionary. A set makes membership O(length) string hash expected.

## Algorithm
1. `wordset = set(words)`, `ok = [False] * (n+1)`, `ok[0] = True`.
2. For `i` in 1..n: `ok[i] = any(ok[j] and s[j:i] in wordset for j in range(i))`.
3. Return `ok[n]`.

## Trace
`s = "leetcode"`, words `["leet","code"]`.

| i | prefix | ok[i] | reason |
|---|---|---|---|
| 0 | "" | T | base |
| 1..3 | l,le,lee | F | no dict word |
| 4 | leet | T | ok[0] + "leet" |
| 5..7 | … | F | |
| 8 | leetcode | T | ok[4] + "code" |

## Complexity
O(n² · L) worst if you slice naively for every `(j,i)` with average slice cost L; with word length limits you can bound inner tries by max word length. Space O(n) for `ok` plus the set. Memoized recursion is the same DAG of indexes.

## Edge cases
Empty `s` → True with empty segmentation. Word longer than `s`. Dictionary contains `s` itself. Leading zeros style traps do not apply; `"applepenapple"` with reuse of `"apple"` and `"pen"` must allow reuse. Characters that never start a word → early False stretch.

## Alternatives and trade-offs
Trie of words + DP on indexes. BFS on break indexes. Recursion + `@cache` is clean in Python. Prefer set+DP in timed challenges for clarity.

## Common bugs
Disallowing word reuse when the prompt allows it. Using `ok[i] = s[:i] in wordset` only (misses multi-word). Off-by-one on `ok` length. Checking `s[i:j]` instead of `s[j:i]`.

## Follow-ups
Word Break II (list all). Concatenated words. Design a system that streams tokens.

## Related problems
Word Break II, Concatenated Words, Palindrome Partitioning, Coin Change (unbounded knapsack cousin).
