# 44. Sliding Window Maximum — walkthrough

## Recognize it
For every contiguous window of size `k`, report the maximum. Look-alike: moving average (sum, not max). Another look-alike: sparse table / RMQ for static queries (different API).

## Brute force
For each window start, scan `k` elements for the max: O(n·k). Too slow when both n and k are large (e.g. 1e5).

## Key insight
Maintain a deque of indexes with values in decreasing order inside the window. The front is always the max. When the front falls out of the window, pop it. Before appending a new index, pop the back while its value is ≤ the new value—those can never be the max while the new one is present.

## Algorithm
1. Empty deque `dq`, result list `out`.
2. For each index `i` with value `v`:
   - While `dq` and `dq[0] <= i - k`: popleft.
   - While `dq` and `nums[dq[-1]] <= v`: pop right.
   - Append `i`.
   - If `i >= k - 1`, append `nums[dq[0]]` to `out`.
3. Return `out`.

## Trace
`nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`.

| i | v | dq (vals) | out |
|---|---|---|---|
| 0 | 1 | [1] | — |
| 1 | 3 | [3] | — |
| 2 | -1 | [3,-1] | [3] |
| 3 | -3 | [3,-1,-3] | [3,3] |
| 4 | 5 | [5] | [3,3,5] |
| 5 | 3 | [5,3] | […,5] |
| 6 | 6 | [6] | […,6] |
| 7 | 7 | [7] | […,7] |

Final `[3,3,5,5,6,7]`.

## Complexity
Each index enters and leaves the deque at most once: O(n) time. Deque holds at most k indexes: O(k) space. Better than O(n·k) scans. A heap with lazy expiry is O(n log n) and fussier.

## Edge cases
`k = 1` → the array itself. `k = n` → one maximum. Strictly decreasing array—deque keeps all k until they age out. Equal values—use `<=` when popping the back so newer equals win and old indexes expire cleanly.

## Alternatives and trade-offs
Sparse table: O(n log n) preprocess, O(1) per window—great for many queries, heavier to code. Segment tree same idea. Heap of pairs `(value, index)` with skip-stale pops works but is slower.

## Common bugs
Storing values instead of indexes so you cannot expire by window bound. Using `<` instead of `<=` and leaving stale equals. Emitting before the first full window (`i >= k-1`). Forgetting to pop the front when `i - k` passes it.

## Follow-ups
Sliding window minimum. Sliding window median. Constrained subsequence sum (monotonic deque DP).

## Related problems
Longest Continuous Subarray With Absolute Diff, Jump Game VI, Daily Temperatures (monotonic stack cousin).
