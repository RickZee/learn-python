# 54. Longest Increasing Subsequence — walkthrough

## Recognize it
Length of the longest strictly increasing subsequence (not necessarily contiguous). Look-alike: longest increasing *subarray* (contiguous). Another look-alike: Russian doll envelopes (LIS after sort).

## Brute force
DP `best[i] = 1 + max(best[j] for j < i if nums[j] < nums[i])`, else 1. O(n²) time—fine up to a few thousand, tight at 1e5.

## Key insight
Patience sorting / tails array: `tails[k]` is the smallest tail of all increasing subsequences of length `k+1`. For each value, binary-search the first tail ≥ value and replace it (or append). Length of `tails` is the LIS length. Strict increase uses `bisect_left`.

## Algorithm
1. `tails = []`.
2. For each `value` in `nums`:
   - `i = bisect_left(tails, value)`.
   - If `i == len(tails)`, append; else `tails[i] = value`.
3. Return `len(tails)`.

## Trace
`nums = [10, 9, 2, 5, 3, 7, 101, 18]`.

| value | tails after |
|---|---|
| 10 | [10] |
| 9 | [9] |
| 2 | [2] |
| 5 | [2,5] |
| 3 | [2,3] |
| 7 | [2,3,7] |
| 101 | [2,3,7,101] |
| 18 | [2,3,7,18] |

Length 4 (e.g. 2,3,7,18).

## Complexity
O(n log n) time, O(n) space for tails. Beats O(n²) DP when n is large (typical challenge limit 1e5). Reconstructing one actual subsequence needs parent pointers or a second structure—length-only is what this prompt asks. The tails array is not itself a valid LIS; it only stores the smallest possible endings for each length.

## Edge cases
Empty → 0. Strictly decreasing → 1. All equal → 1 for strict LIS. Single element. Duplicates: `bisect_left` replaces equals so length does not grow.

## Alternatives and trade-offs
Classic O(n²) DP is easier to prove and extend to counts. Fenwick/segment tree on compressed values also O(n log n). For non-decreasing LIS use `bisect_right`.

## Common bugs
Using `bisect_right` for strict LIS (treats equals wrong). Returning `tails` itself as a subsequence (it is not necessarily one LIS). Off-by-one length. Contiguous-only scan.

## Follow-ups
Return one LIS, not only length. Number of LIS. Longest decreasing. Envelopes / box stacking.

## Related problems
Russian Doll Envelopes, Number of Longest Increasing Subsequence, Maximum Length of Pair Chain, Longest Common Subsequence.
