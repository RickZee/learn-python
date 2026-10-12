# 07. Merge Intervals — walkthrough

## Recognize it
Overlapping or touching intervals should become one. Sort by start, then extend or append. Look-alike: insert interval (one new interval into a sorted list).

## Brute force
Compare every pair and merge repeatedly until stable: worse than O(n²) in practice.

## Key insight
After sorting by start, you only need to compare each interval to the last merged one. If it overlaps or touches, extend the end; otherwise append.

## Algorithm
1. Sort intervals by start.
2. Seed `merged` with the first interval copy.
3. For each next span, if `start <= merged[-1][1]`, set end to max; else append a copy.
4. Return `merged` (empty input → `[]`).

## Trace
`[[1,3],[2,6],[8,10],[15,18]]` sorted same.

| next | merged |
|---|---|
| [1,3] | [[1,3]] |
| [2,6] | [[1,6]] |
| [8,10] | [[1,6],[8,10]] |
| [15,18] | [[1,6],[8,10],[15,18]] |

## Complexity
O(n log n) for the sort, O(n) merge pass. Space O(n) for the answer.

## Edge cases
Empty list. Single interval. Nested intervals. Touching ends (`[1,2],[2,3]` → `[1,3]`).

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure. Sweep line with +1/-1 events also works and generalizes to counting overlaps (Meeting Rooms II). Sorting by end is wrong for this merge rule.

## Common bugs
Sorting by end. Using `<` instead of `<=` so touching intervals stay split. Mutating the input without copying.

## Follow-ups
Insert Interval. Meeting Rooms II (min rooms). Merge accounting for open/closed ends.

## Related problems
Insert Interval, Meeting Rooms, Non-overlapping Intervals.
