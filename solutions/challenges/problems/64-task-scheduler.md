# 64. Task Scheduler — walkthrough

## Recognize it
Tasks are letters; identical tasks need `n` cool-down units between runs. Idle slots fill the gaps. Return the minimum intervals to finish all tasks. Look-alike: rearrange string k distance apart (related greedy). Another look-alike: CPU scheduling with different priorities.

## Brute force
Simulate a max-heap of remaining counts each time unit, picking a ready task—O(time · log 26). Correct but longer to implement; the closed formula below matches the optimum for this problem.

## Key insight
The most frequent task sets a skeleton of `peak` frames separated by `n` idles: `(peak - 1) * (n + 1)` slots for the first `peak-1` occurrences, then `peak_count` slots for the last occurrence of every task that also has frequency `peak`. If other tasks fill the idles, the answer is just `len(tasks)`. So take the max of those two quantities.

## Algorithm
1. Count frequencies; `peak = max(counts)`; `peak_count =` how many tasks hit `peak`.
2. Return `max(len(tasks), (peak - 1) * (n + 1) + peak_count)`.

## Trace
`tasks = ["A","A","A","B","B","B"]`, `n = 2`.

`peak = 3`, `peak_count = 2` (A and B).

Formula: `(3-1)*(2+1)+2 = 8`. Schedule sketch `A B _ A B _ A B` — length 8. `len(tasks)=6`, so answer 8.

| n | formula | note |
|---|---|---|
| 0 | max(6, (3-1)*1+2)=6 | no cool-down |
| 2 | 8 | idles needed |
| 50 | (3-1)*51+2=104 | large cool-down dominates len(tasks) |

## Complexity
O(T) to count T tasks (alphabet fixed 26). O(1) extra beyond the counter. Simulation with a heap is O(T log Σ) and easier to adapt if constraints change.

## Edge cases
`n = 0` → `len(tasks)`. One task type only → `(peak-1)*(n+1)+1`. All unique tasks → `len(tasks)`. Many tasks that fill all idle gaps → answer equals `len(tasks)`.

## Alternatives and trade-offs
Heap simulation is the safe explanation when you forget the formula. Formula is fastest once you trust the skeleton argument. Neither needs true time-step loops for the return value alone.

## Common bugs
Using `peak * (n+1)` without the `-1` adjustment. Forgetting `peak_count` when several tasks share the max frequency. Returning only the formula when `len(tasks)` is larger. Cool-down off-by-one (`n` vs `n+1` frame width).

## Follow-ups
Rearrange string k distance apart. Maximum frequency stack. Hand of straights.

## Related problems
Rearrange String k Distance Apart, Maximum Number of Events, Course Schedule III.
