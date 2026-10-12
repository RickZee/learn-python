# 63. Longest Palindromic Substring — walkthrough

## Recognize it
Return any longest substring that reads the same forward and backward. Look-alike: longest palindromic subsequence (not contiguous). Another look-alike: palindrome partition (cut into palindromes).

## Brute force
Check every substring `s[i:j]` for palindrome; keep the longest. O(n²) substrings × O(n) check = O(n³), or O(n²) with early expand. Too slow if you re-check from scratch each time without expand.

## Key insight
Every palindrome expands from a center. There are `2n-1` centers: each index (odd length) and each gap between indexes (even length). Expand while left and right characters match; track the best `[start, end]`.

## Algorithm
1. If `s` empty, return `""`. `start = end = 0`.
2. `expand(L, R)`: while in bounds and equal, `L-=1`, `R+=1`; return the inclusive ends inside the last success.
3. For each `i`: expand `(i,i)` and `(i,i+1)`; if wider than `[start,end]`, replace.
4. Return `s[start:end+1]`.

## Trace
`s = "babad"`.

| center | expand result | best |
|---|---|---|
| i=0 'b' | "b" | b |
| gap 0-1 | no | b |
| i=1 'a' | "bab" | bab |
| gap 1-2 | "aba" (same len) | bab or aba |
| i=2 'b' | "babad" no; "bab"/"aba" already covered | … |
| … | | length 3 |

One valid answer `"bab"` or `"aba"`.

## Complexity
O(n) centers × O(n) expand = O(n²) time, O(1) extra space. Manacher's algorithm is O(n) but rarely required. DP table `P[i][j]` is O(n²) time and space.

## Edge cases
Empty string. Single character. Whole string palindrome. Even-length longest (`"cbbd"` → `"bb"`). Multiple answers of equal length—any is fine. All identical characters.

## Alternatives and trade-offs
DP boolean table is clear for teaching. Manacher for strict linear time. Prefer center expand in timed challenges: short and O(1) space.

## Common bugs
Only expanding odd centers (misses `"bb"`). Returning indexes after one extra decrement without `+1`/`-1`. Comparing length with `<` so ties never update (still correct) vs forgetting to update on longer. Mutating `s`.

## Follow-ups
Count all palindromic substrings (same expand). Longest palindromic subsequence. Min cuts for palindrome partition.

## Related problems
Palindromic Substrings, Longest Palindromic Subsequence, Valid Palindrome, Palindrome Partitioning.
