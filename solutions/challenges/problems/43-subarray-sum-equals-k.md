# 43. Subarray Sum Equals K — walkthrough

## Recognize it
Count contiguous subarrays whose values sum to `k`. Array may contain negatives, so a shrinking sliding window on sums is wrong. Look-alike: longest subarray with sum k (same prefix idea, track earliest index). Another look-alike: two sum on prefixes.

## Brute force
For every `i`, expand `j` from `i` and add; when the running sum equals `k`, increment. O(n²) time. Fine for tiny n; fails at n ~ 1e5.

## Key insight
If `prefix[j] - prefix[i] = k`, then the subarray `(i+1)..j` sums to `k`. While scanning, at prefix `total`, you need how many earlier prefixes equalled `total - k`. A hash map from prefix sum → count answers that in expected O(1). Seed the map with `{0: 1}` so subarrays that start at index 0 are counted.

## Algorithm
1. `counts = {0: 1}`, `total = 0`, `answer = 0`.
2. For each value: `total += value`; `answer += counts[total - k]`; `counts[total] += 1`.
3. Return `answer`.

## Trace
`nums = [1, 2, 3]`, `k = 3`.

| value | total | total-k | counts before | add | counts after |
|---|---|---|---|---|---|
| 1 | 1 | -2 | {0:1} | 0 | {0:1,1:1} |
| 2 | 3 | 0 | … | 1 ([1,2]) | {0:1,1:1,3:1} |
| 3 | 6 | 3 | … | 1 ([3]) | {…,6:1} |

Answer 2. Note `[1,2]` and `[3]` both work; `[1,2,3]` sums to 6 ≠ 3.

## Complexity
One pass: O(n) time. Map holds at most n+1 keys: O(n) space. Required when negatives appear; a two-pointer window assumes non-negative nums.

## Edge cases
`k = 0` and zeros in the array—many empty-looking prefixes; the map handles them. Single element equal to `k`. Entire array sums to `k`. Negatives that make the same prefix repeat—use counts, not a set. Empty array → 0.

## Alternatives and trade-offs
O(n²) nested loops for teaching. If all values are positive, a sliding window can find whether a subarray sums to `k`, but counting all still needs care. Segment trees are overkill here.

## Common bugs
Forgetting `counts[0] = 1`. Updating the map before querying `total - k` (double-counts the empty contribution wrong for some k). Using a set of prefixes when duplicates matter. Sliding window with negatives.

## Follow-ups
Subarray sum equals k with at most / exactly distinct count. Continuous subarray sum (divisible by k). Longest well-forming subarray.

## Related problems
Two Sum, Contiguous Array (0/1), Path Sum III (same idea on trees), Product of Array Except Self.
