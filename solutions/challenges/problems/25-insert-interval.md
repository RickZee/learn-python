# 25. Insert Interval — walkthrough

## Recognize it
You already have a list of non-overlapping intervals sorted by start. Insert one new interval and merge whatever overlaps so the result stays sorted and non-overlapping. Look-alike: merge intervals from an unsorted bag (sort first, then merge everything). Another look-alike: meeting rooms (detect overlap without producing a merged list).

## Brute force
Append `new` to the list, sort by start, then run the standard merge-intervals scan. Correct, but sorting makes it O(n log n) even though the input was already sorted. When n is large and you only add one interval, a linear merge without re-sorting is the intended win.

## Key insight
Because the list is sorted and non-overlapping, every interval falls into exactly one of three phases relative to `new`: completely to the left (ends before `new` starts), overlapping or touching `new`, or completely to the right (starts after `new` ends). Copy left, fold all overlapping into an expanding `new`, append the merged span, then copy the right tail.

## Algorithm
1. `result = []`, `index = 0`.
2. While `index < n` and `intervals[index][1] < new[0]`: append that interval; advance. (Strictly left; a shared endpoint merges in the next phase.)
3. While `index < n` and `intervals[index][0] <= new[1]`: set `new = [min(starts), max(ends)]`; advance.
4. Append the (possibly expanded) `new`.
5. Extend with `intervals[index:]` and return.

## Trace
`intervals = [[1,3],[6,9]]`, `new = [2,5]`.

| phase | index | new | result |
|---|---|---|---|
| left scan | 0 | [2,5] | [] (1,3 ends at 3, not < 2) |
| merge | 0→1 | [1,5] | [] |
| merge stops | 1 | [1,5] | — (6 ≰ 5? 6 > 5) |
| append new | 1 | — | [[1,5]] |
| copy rest | — | — | [[1,5],[6,9]] |

Touching case: `[[1,2],[3,5]]` insert `[2,3]` → merge both into `[1,5]` because `2 <= 2` and later `3 <= 3`.

## Complexity
One pass over n intervals: O(n) time. Output list O(n) space. Avoids the O(n log n) sort of "append then full merge." Only worth sorting again if the input was not already sorted.

## Edge cases
Empty `intervals` → `[new]`. New completely before or after everything → insert at ends without merging. New swallows several intervals in the middle. Touching endpoints (`[1,2]` and `[2,3]`) merge when you use `<=` on the overlap test and `<` on the left-copy test. New equal to an existing interval → that one interval remains.

## Alternatives and trade-offs
Append + sort + merge is shorter if you already have merge-intervals code and n is tiny. Binary search for the first overlapping index can find the splice point in O(log n), but you still spend O(n) copying the result—rarely worth the extra code unless the API is insert-into-a-tree of intervals.

## Common bugs
Using `<=` when copying the left side so a touching interval is skipped and never merged. Forgetting to append `new` when it overlaps nothing. Mutating the caller's list in place when the prompt wants a new list. Off-by-one when `new` sits between two intervals with a gap.

## Follow-ups
Range module (add/remove/query). Merge intervals (unsorted). Employee free time (gaps across multiple calendars).

## Related problems
Merge Intervals, Non-overlapping Intervals, Meeting Rooms II, Range Module.
