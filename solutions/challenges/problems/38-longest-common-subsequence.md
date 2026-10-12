# 38. Longest Common Subsequence — walkthrough

## Recognize it
Two strings; length of the longest sequence of characters that appears in both in order, not necessarily contiguous. Look-alike: longest common substring (must be contiguous—different recurrence). Another look-alike: edit distance (related table, different scoring).

## Brute force
For every subsequence of `text1`, check whether it is a subsequence of `text2`, keep the longest. There are 2^len(text1) subsequences, so exponential. Recursing on prefixes without memo hits the same pair of indexes repeatedly.

## Key insight
Let `dp[i][j]` be the LCS length of `text1[:i]` and `text2[:j]`. If the last characters match, `dp[i][j] = dp[i-1][j-1] + 1`. Otherwise take `max(dp[i-1][j], dp[i][j-1])`—drop a character from one side. Only the previous row is needed for the next row.

## Algorithm
1. `previous = [0] * (len(text2) + 1)`.
2. For `i` from 1 to len(text1):
   - Build `current` of zeros, length len(text2)+1.
   - For `j` from 1 to len(text2): if characters match, `current[j] = previous[j-1] + 1`; else `current[j] = max(previous[j], current[j-1])`.
   - Set `previous = current`.
3. Return `previous[-1]`.

## Trace
`text1 = "abcde"`, `text2 = "ace"`.

After processing `"a"` / `"ace"`: previous ends `[0,1,1,1]`.
After `"ab"`: still length 1 through `"ace"`.
After `"abc"`: when `c` matches `c`, diagonal+1 → length 2 at the end of `"ac"`.
After `"abcd"`: unchanged 2.
After `"abcde"`: `e` matches `e` → length 3.

| i (prefix of text1) | LCS vs "ace" |
|---|---|
| a | 1 ("a") |
| ab | 1 |
| abc | 2 ("ac") |
| abcd | 2 |
| abcde | 3 ("ace") |

## Complexity
Every pair of prefixes is filled once: O(len(text1)·len(text2)) time. One or two rows of length len(text2)+1: O(len(text2)) space. Full table uses O(len(text1)·len(text2)) space if you need to reconstruct the string.

## Edge cases
Either string empty → 0. Identical strings → full length. No shared characters → 0. Single shared character anywhere. Longer string first vs second—swap rows if you want the shorter as the rolling dimension.

## Alternatives and trade-offs
Full 2D table is clearer for reconstruction (walk back from the corner). Recursive memo on `(i, j)` matches the recurrence. Hirschberg's algorithm gets the actual LCS in linear space with more code—rarely asked. Do not confuse with substring DP that resets on mismatch.

## Common bugs
Using contiguous matching (substring) so a gap kills the count. Writing `previous[j] + 1` instead of `previous[j-1] + 1` on a match. Forgetting the +1 padding row/column of zeros. Mutating one row in place without a temp and reading a already-updated neighbor as if it were the previous row.

## Follow-ups
Return the LCS string, not only the length. Longest common substring. Shortest common supersequence. Diff of two files.

## Related problems
Edit Distance, Longest Palindromic Subsequence, Delete Operation for Two Strings, Longest Increasing Subsequence.
