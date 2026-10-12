# 57. Edit Distance — walkthrough

## Recognize it
Minimum insertions, deletions, and substitutions to turn `word1` into `word2`. Look-alike: longest common subsequence (related: edits ≈ m+n-2·LCS when only insert/delete). Another look-alike: one-edit distance (boolean, shorter).

## Brute force
Recurse on suffixes: if heads match, advance both; else try insert, delete, replace and take 1+min. Without memo, branching is exponential.

## Key insight
`dp[i][j]` = edit distance of `word1[:i]` and `word2[:j]`. Match → `dp[i-1][j-1]`; else `1 + min(replace, delete, insert)` = `1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])`. One rolling row stores the previous `i`, with careful use of a `prev` diagonal.

## Algorithm
1. `dp = list(range(n+1))` — distances from empty `word1` prefix to `word2` prefixes.
2. For `i` in 1..m:
   - Save `prev = dp[0]`; set `dp[0] = i`.
   - For `j` in 1..n: keep `cur = dp[j]`; if chars match, `dp[j] = prev`; else `dp[j] = 1 + min(prev, dp[j], dp[j-1])`; `prev = cur`.
3. Return `dp[n]`.

## Trace
`word1 = "horse"`, `word2 = "ros"`.

After full fill (conceptual 2D corner):

|  | "" | r | o | s |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| h | 1 | 1 | 2 | 3 |
| ho | 2 | 2 | 1 | 2 |
| hor | 3 | 2 | 2 | 2 |
| hors | 4 | 3 | 3 | 2 |
| horse | 5 | 4 | 3 | **3** |

Path example: horse → rorse → rose → ros (3 edits).

## Complexity
O(m·n) time, O(n) space with one row (O(m·n) for full table if you need the alignment). LCS-based formula only covers insert/delete unless you model replace separately.

## Edge cases
Either string empty → length of the other. Identical strings → 0. One character differ. Classic `"intention"` / `"execution"`. Very unequal lengths.

## Alternatives and trade-offs
Full 2D table is easiest to explain. Ukkonen's algorithms and Meyers diff are for specialists. Recursion + cache matches the recurrence. Prefer rolling row when memory matters.

## Common bugs
Forgetting the diagonal `prev` when compressing to one row. Initializing `dp` wrong. Using LCS length as the answer directly. Off-by-one on empty prefixes.

## Follow-ups
Recover the edit script. Only allow insert/delete. Fuzzy match threshold (early abort).

## Related problems
Longest Common Subsequence, One Edit Distance, Delete Operation for Two Strings, Shortest Common Supersequence.
