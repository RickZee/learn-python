# 21. Maximum Subarray — walkthrough

## Recognize it
Given a non-empty integer array that may contain negatives, return the largest sum of any contiguous subarray. The subarray must be non-empty. Look-alike: maximum subsequence sum without requiring contiguity (then just sum positives). Another look-alike: maximum product subarray, which needs separate tracking for sign flips.

## Brute force
For every pair of ends `(i, j)`, sum `nums[i..j]` and keep the max. Naïve summing is O(n³); with prefix sums or a running sum per i it becomes O(n²). Still too slow for large n (1e5).

## Key insight
Kadane's idea: as you scan, maintain `current` = best subarray sum ending at this index. That is either `value` alone (start fresh) or `current + value` (extend). Then `best` is the max of all those ending sums. You abandon a prefix when it cannot help future endings—specifically when the running sum before this value is negative, extending would only hurt, so starting over at `value` wins.

## Algorithm
1. Set `best = current = nums[0]`.
2. For each `value` in `nums[1:]`:
   - `current = max(value, current + value)`.
   - `best = max(best, current)`.
3. Return `best`.

## Trace
`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`.

| value | current | best |
|---|---|---|
| -2 | -2 | -2 |
| 1 | 1 | 1 |
| -3 | -2 | 1 |
| 4 | 4 | 4 |
| -1 | 3 | 4 |
| 2 | 5 | 5 |
| 1 | 6 | 6 |
| -5 | 1 | 6 |
| 4 | 5 | 6 |

Winning segment `4 + -1 + 2 + 1 = 6`.

## Complexity
One pass: O(n) time, O(1) space. Divide-and-conquer (max on left, right, or crossing mid) is O(n log n)—good for teaching recursion, slower and longer to code. Prefix-sum scanning every end is O(n²).

## Edge cases
All negative: answer is the largest (least negative) single element—because `current = max(value, current+value)` still considers singletons. Single element → that element. Zeros: a zero can end a run or start a fresh zero segment. Empty array is usually disallowed; if allowed, define the prompt's convention.

## Alternatives and trade-offs
Prefix sums + min prefix so far: `best = max(prefix[j] - min_prefix_before_j)`. Same O(n). Divide-and-conquer is classic textbook. Returning indices as well needs to store start markers when you reset `current`. For circular maximum subarray, combine total sum with min subarray—different problem.

## Common bugs
Resetting when `current` hits 0 instead of when extending loses—then all-negative arrays wrongly become 0 if 0 is not in the array. Initializing `best = 0`, which rejects negative-only inputs. Using `current + value` without the `max(value, …)` restart. Confusing with non-contiguous "max sum of any subset."

## Follow-ups
Return the start and end indexes. Maximum product subarray. Maximum sum circular subarray. k-concatenated array variants.

## Related problems
Best Time to Buy and Sell Stock (delta Kadane), House Robber (non-contiguous), Jump Game, Trapping Rain Water.
