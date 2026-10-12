# 46. Koko Eating Bananas — walkthrough

## Recognize it
Piles of bananas; speed `k` means each pile of size `p` takes `ceil(p / k)` hours, and piles are eaten one after another. Find the minimum integer speed that finishes within `h` hours. Look-alike: split array largest sum (binary search on answer with a different feasibility). Another look-alike: capacity to ship packages in d days.

## Brute force
Try every speed from 1 to `max(piles)` and compute hours; return the smallest that fits. That is O(max(piles) · n)—too slow when piles can be 1e9.

## Key insight
Hours as a function of speed is monotonically non-increasing: faster never hurts. Binary search the smallest speed where `hours(speed) <= h`. Feasibility is a linear scan with integer ceiling `(p + speed - 1) // speed`.

## Algorithm
1. `lo, hi = 1, max(piles)`.
2. While `lo < hi`:
   - `mid = (lo + hi) // 2`.
   - If `hours(mid) <= h`, search left including mid (`hi = mid`); else `lo = mid + 1`.
3. Return `lo`.

## Trace
`piles = [3, 6, 7, 11]`, `h = 8`.

| lo | hi | mid | hours(mid) | action |
|---|---|---|---|---|
| 1 | 11 | 6 | ceil 3/6+6/6+7/6+11/6 = 1+1+2+2 = 6 ≤ 8 | hi=6 |
| 1 | 6 | 3 | 2+2+3+4 = 11 > 8 | lo=4 |
| 4 | 6 | 5 | 1+2+2+3 = 8 ≤ 8 | hi=5 |
| 4 | 5 | 4 | 1+2+2+3 = 8 ≤ 8 | hi=4 |

Answer 4.

## Complexity
O(n log M) time where M = max(piles): log M binary steps, each scans n piles. O(1) extra space. Linear search over speeds would be O(n·M).

## Edge cases
`h == len(piles)` → must eat one pile per hour at speed `max(piles)`. `h` very large → speed 1. Single pile. Piles of size 1. Off-by-one using `/` float ceiling instead of integer formula.

## Alternatives and trade-offs
Lower bound can be `ceil(sum(piles) / h)` instead of 1—same log factor, fewer iterations. Ternary search is unnecessary on an integer monotone predicate. Simulation with a heap is the wrong pattern here.

## Common bugs
`lo <= hi` with `hi = mid - 1` but returning the wrong side. Using `math.ceil(p / speed)` with true division and float error on huge piles. Comparing `hours < h` instead of `<=`. Setting `hi` to `sum(piles)` without need.

## Follow-ups
Minimum speed to arrive on time (LeetCode variant with dist/hours). Split array largest sum. Kth missing number (different binary search).

## Related problems
Capacity To Ship Packages, Split Array Largest Sum, Magnetic Force Between Two Balls, Find Minimum in Rotated Sorted Array (index-space vs answer-space).
