# 45. Longest Repeating Character Replacement — walkthrough

## Recognize it
Longest substring you can make all one character by changing at most `k` other characters. Look-alike: longest substring with at most k distinct characters (different budget). Another look-alike: minimum window cover (shrink when valid, here you expand while valid).

## Brute force
For every substring, count the most frequent character; if `length - max_freq <= k`, it is valid—track the max length. O(n² · alphabet) with recounting, or O(n²) with rolling counts still too slow for large n.

## Key insight
In a window, you keep the majority character and rewrite everything else. The window is valid while `window_len - max_count <= k`. Expand right; when invalid, advance left. You never need to decrease `max_count` when shrinking for the *length* answer—`max_count` is a historical max that only makes the validity test stricter, which is safe because you only care about the longest window ever seen.

## Algorithm
1. `counts` map, `left = 0`, `best = 0`, `max_count = 0`.
2. For `right, ch` in enumerate(`s`):
   - `counts[ch] += 1`; `max_count = max(max_count, counts[ch])`.
   - While `right - left + 1 - max_count > k`: decrement `counts[s[left]]`; `left += 1`.
   - `best = max(best, right - left + 1)`.
3. Return `best`.

## Trace
`s = "AABABBA"`, `k = 1`.

| right | ch | window | max_count | len-max | best |
|---|---|---|---|---|---|
| 0 | A | A | 1 | 0 | 1 |
| 1 | A | AA | 2 | 0 | 2 |
| 2 | B | AAB | 2 | 1 | 3 |
| 3 | A | AABA | 3 | 1 | 4 |
| 4 | B | AABAB → shrink | 3 | … | 4 |
| … | | BABBA windows | | | 4 |

Best 4 (`AABA` → all A with one change, or `ABBA` similarly).

## Complexity
Each endpoint moves at most n times: O(n) time for fixed alphabet. Counts map O(alphabet) space. The O(n²) check of every substring is the brute baseline you beat.

## Edge cases
`k = 0` → longest run of identical characters. `k >= n` → n. Single character string. All unique letters with small k. Uppercase-only vs mixed—map keys handle both.

## Alternatives and trade-offs
Recomputing the true max in the window after every shrink is O(26) and also correct; skipping the decrease of `max_count` is a known optimization that still yields the correct *length*. Binary search on length + feasibility is O(n log n).

## Common bugs
Using distinct-character budget instead of replacement budget. Shrinking with a stale count for the left character. Forcing `max_count` to decrease and then getting off-by-ones. Returning the number of changes instead of the length.

## Follow-ups
Replace to make palindrome with ≤ k changes. Longest substring with at most k distinct. Max consecutive ones with at most k flips.

## Related problems
Longest Substring with At Most K Distinct, Max Consecutive Ones III, Minimum Window Substring.
