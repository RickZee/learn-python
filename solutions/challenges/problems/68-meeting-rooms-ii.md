# 68. Meeting Rooms II — walkthrough

## Recognize it
Given meeting intervals `[start, end)`, find the minimum number of rooms so no two overlapping meetings share a room. Look-alike: meeting rooms I (boolean can-attend-all). Another look-alike: merge intervals (produce merged spans, not room count).

## Brute force
Sort by start; for each meeting scan all earlier end times for a free room—O(n²). Or assign each meeting a room id greedily with a list of end times scanned linearly.

## Key insight
Sort meetings by start. Keep a min-heap of end times of rooms currently occupied. When a meeting starts, if the earliest end ≤ start, that room frees and you reuse it (pop). Always push the new meeting's end. The heap size is the number of rooms in use; the maximum size is the answer—and because we only pop when free, the final size equals the peak.

## Algorithm
1. If no intervals, return 0. Sort by start.
2. `rooms` min-heap empty.
3. For each `(start, end)`: if heap and `rooms[0] <= start`, pop; push `end`.
4. Return `len(rooms)`.

## Trace
`[[0,30],[5,10],[15,20]]`.

| meeting | heap ends before | action | heap after |
|---|---|---|---|
| [0,30] | [] | push 30 | [30] |
| [5,10] | [30] (30>5) | push 10 | [10,30] |
| [15,20] | [10,30] (10≤15) | pop 10, push 20 | [20,30] |

Answer 2.

## Complexity
O(n log n) for sort and heap ops. O(n) space for the heap. Sweep line with sorted starts and ends also O(n log n): +1 at start, -1 at end, track peak.

## Edge cases
Empty list → 0. No overlaps → 1. All overlap → n. Touching endpoints (`[1,2]` and `[2,3]`) reuse a room when using `<=` on end vs start (half-open intervals). Unsorted input—must sort.

## Alternatives and trade-offs
Two sorted arrays of starts and ends with two pointers is a classic sweep without a heap. Chronological events `(time, delta)` sorted with ends before starts at the same time for half-open reuse. Prefer heap when you also want to know which room.

## Common bugs
Sorting by end instead of start. Using `<` instead of `<=` so touching meetings take an extra room (or the reverse, depending on closed/open). Pushing starts instead of ends. Returning the number of pop operations.

## Follow-ups
Meeting Rooms III (track delays). Car pooling (same sweep with capacity). Minimum platforms for trains.

## Related problems
Merge Intervals, Non-overlapping Intervals, Car Pooling, Employee Free Time.
