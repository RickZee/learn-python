# 18. House Robber — walkthrough

## Recognize it
Houses stand in a line with non-negative loot values. You may rob a subset of houses, but you cannot rob two adjacent ones. Maximize total loot. Empty street means 0. Look-alike: house robber II (houses in a circle—first and last are adjacent). Another look-alike: maximum subarray, which requires a contiguous block; here the chosen houses need not be contiguous, only non-adjacent.

## Brute force
For each house, decide rob or skip, recurse on the rest, and take the max—2ⁿ subsets, exponential. You can prune when you skip after a rob, but the raw tree is still exponential without memoization. For n = 40 that is hopeless.

## Key insight
At house i with value v, the best total ending at this decision is `max(best_without_taking_i, best_ending_before_i-1 + v)`. Rolling two scalars is enough: `previous` = best through the house before last, `current` = best through the last house considered. When you process v, the new best is `max(current, previous + v)`.

## Algorithm
1. Set `previous = 0`, `current = 0`.
2. For each `value` in `nums`:
   - `previous, current = current, max(current, previous + value)`.
3. Return `current`.

Reading the update: `current` (old) is "skip this house"; `previous + value` is "take this house and add the best from two ago."

## Trace
`nums = [2, 7, 9, 3, 1]`.

| value | previous | current before | take | skip | current after |
|---|---|---|---|---|---|
| 2 | 0 | 0 | 0+2=2 | 0 | 2 |
| 7 | 2 | 2 | 0+7=7 | 2 | 7 |
| 9 | 7 | 7 | 2+9=11 | 7 | 11 |
| 3 | 11 | 11 | 7+3=10 | 11 | 11 |
| 1 | 11 | 11 | 11+1=12 | 11 | 12 |

Optimal plan: 2 + 9 + 1 = 12 (houses 0, 2, 4).

## Complexity
One pass: O(n) time, O(1) extra space. A DP array `dp[i]` = best using the first i houses is O(n) space and the same time—clearer for teaching, same asymptotics. Brute subsets are exponential and only useful as a correctness story for tiny n.

## Edge cases
Empty list → 0. Single house → that value. Two houses → `max` of them. All zeros → 0. Increasing then drop (as above) needs the skip branch. Negative values are usually excluded by the prompt; if present, treat carefully because "rob" could hurt.

## Alternatives and trade-offs
Explicit `dp` array aids debugging and proofs. Memoized recursion from index i ("best from i onward") is natural top-down. For the circular variant, run the linear solver twice (drop first, drop last) and take the max—do not force one pass with ad hoc wrap logic. Bitmask DP is overkill for a line.

## Common bugs
Using `previous + value` without also considering `current` (always robbing when you should skip). Initializing from `nums[0]` incorrectly when the list is empty. Confusing adjacency: skipping one house is allowed; you do not need to rob every other house starting at 0. Porting the circular rule into the linear problem by excluding the last house always.

## Follow-ups
House Robber II (circle). House Robber III (binary tree). Delete and earn (reduce to robber on value line). Max sum with no two adjacent in a circular array.

## Related problems
Climbing Stairs (same rolling recurrence shape), Maximum Subarray (contiguous), Coin Change (unbounded knapsack DP), Jump Game (linear decisions).
