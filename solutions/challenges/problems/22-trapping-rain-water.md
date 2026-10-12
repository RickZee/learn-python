# 22. Trapping Rain Water — walkthrough

## Recognize it
An elevation map is given as non-negative bar heights of width 1. Water sits in valleys: above index i the water depth is `min(tallest_left, tallest_right) - height[i]` when that quantity is positive. Sum the water over all indexes. Look-alike: container with most water (maximize one rectangle between two lines, not sum trapped units). Another look-alike: largest rectangle in histogram (areas of bars, not water).

## Brute force
For each index i, scan left for max height and right for max height, add `max(0, min(left_max, right_max) - height[i])`. That is O(n²) time. Precomputing prefix max and suffix max arrays drops it to O(n) time and O(n) space—already a solid answer. Two pointers squeeze the extra arrays away.

## Key insight
Water at a cell is limited by the shorter of the two bounding maxima. With pointers at both ends, the side with the smaller height can safely compute its water against its own running max: the other side is at least as tall as the current edge, so it is a valid bound. Advance the shorter side, update that side's max, and add water.

## Algorithm
1. Set `left = 0`, `right = n - 1`, `left_max = right_max = water = 0`.
2. While `left < right`:
   - If `height[left] < height[right]`:
     - `left_max = max(left_max, height[left])`
     - `water += left_max - height[left]`
     - `left += 1`
   - Else do the symmetric updates on `right` / `right_max` and decrement `right`.
3. Return `water`.

## Trace
`height = [0,1,0,2,1,0,1,3,2,1,2,1]`.

Two-pointer sketch of early steps (left side moves while left edge is shorter):

| left | right | height[L], height[R] | left_max | add | water |
|---|---|---|---|---|---|
| 0 | 11 | 0, 1 | 0 | 0 | 0 |
| 1 | 11 | 1, 1 | 1 | 0 | 0 |
| 1 | 10 | 1, 2 | 1 | (right side…) | … |

Full prefix/suffix check for the classic figure totals **6** units: valleys between the rising 2 and the peak 3 hold the water. Prefer verifying with the O(n) prefix/suffix arrays on paper when learning, then trust the two-pointer advances.

Concrete small case `height = [4, 1, 2]`:

| step | action | water |
|---|---|---|
| L=0,R=2 (4 vs 2) | right_max=2, add 0, R→1 | 0 |
| L=0,R=1 (4 vs 1) | right_max=2, add 2-1=1, R→0 | 1 |

Stop when pointers meet. Answer 1 (one unit above the middle 1).

## Complexity
Two pointers: O(n) time, O(1) extra space. Prefix + suffix maxima: O(n) time and O(n) space—often clearer in timed challenges if O(1) space is not required. Brute per-index scans are O(n²).

## Edge cases
Fewer than three bars → 0 water. Strictly increasing or decreasing → 0. Flat plateau → 0. Tall walls on both ends with zeros in the middle → deep pool. Single peak in the middle does not trap by itself without higher bounds on both sides.

## Alternatives and trade-offs
Prefix/suffix arrays are the clearest correctness argument. Monotonic stack can compute "next greater" style spans and accumulate water in O(n). Two pointers win on space. Prefer explaining the shorter-side bound aloud so the prompt sees why moving that pointer is safe.

## Common bugs
Adding water on a side before updating that side's max (uses a stale bound). Moving the taller pointer first, which breaks the "other side is high enough" argument. Using `max` of the two heights instead of `min` for the water ceiling. Off-by-one when `left == right`.

## Follow-ups
Trapping rain water in 2D (priority-queue flood from borders). Container with most water. Largest rectangle in histogram (stack).

## Related problems
Container With Most Water, Largest Rectangle in Histogram, Daily Temperatures (monotonic stack), Merge Intervals (geometry on a line).
