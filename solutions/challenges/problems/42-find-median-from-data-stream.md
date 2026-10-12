# 42. Find Median from Data Stream — walkthrough

## Recognize it
Numbers arrive one at a time; after each insert you may be asked for the median of everything so far. Look-alike: median of a static array (sort once). Another look-alike: sliding-window median (also two heaps, but with lazy deletes).

## Brute force
Keep a list, sort before every `find_median`: O(n log n) per query. Insert into a sorted list with `bisect`: O(n) per insert. Both fail when n is large and calls interleave.

## Key insight
Split the stream into a low half and a high half. A max-heap (`low`, store negated values in Python) holds the smaller half; a min-heap (`high`) holds the larger half. Balance so `len(low)` is equal to `len(high)` or one larger. The median is the top of `low`, or the average of both tops when sizes match.

## Algorithm
1. On `add_num(x)`: push `-x` onto `low`; move the largest of `low` into `high` (push `-heappop(low)`); if `high` is bigger than `low`, move one back.
2. On `find_median()`: if `len(low) > len(high)`, return `-low[0]`; else return `(-low[0] + high[0]) / 2`.

## Trace
Add 1, 2, 3; read medians along the way.

| add | low (as values) | high | median |
|---|---|---|---|
| 1 | [1] | [] | 1 |
| 2 | [1] | [2] | 1.5 |
| 3 | [2,1] | [3] | 2 |

After 3: low tops at 2, high at 3, odd count → 2.

## Complexity
Each add does a constant number of heap operations: O(log n). Median read is O(1). Space O(n) for all numbers. Sorted-list insert is O(n) and loses for large streams.

## Edge cases
Single element. All equal values. Strictly increasing or decreasing streams (heaps still rebalance). Even count → average of two middles (float). Negatives and zeros.

## Alternatives and trade-offs
`SortedList` from a third-party library is shorter but not stdlib. Order-statistic trees give the same bounds with more code. Re-sorting is only acceptable for tiny demos.

## Common bugs
Letting one heap lead by more than one element. Forgetting to negate for the max-heap. Averaging with integer division. Pushing into `high` first without the rebalance dance so order breaks. Returning `low[0]` without negating.

## Follow-ups
Sliding window median. Median of two sorted arrays (different problem). Mode / percentiles with count structures.

## Related problems
Sliding Window Median, Kth Largest in a Stream, IPO, Find Median of Two Sorted Arrays.
