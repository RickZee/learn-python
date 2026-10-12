# 47. Jump Game — walkthrough

## Recognize it
Array of jump lengths; from index `i` you may jump to any index in `i .. i+nums[i]`. Can you reach the last index? Look-alike: jump game II (minimum jumps—still greedy, different metric). Another look-alike: BFS levels on indexes when you need distances.

## Brute force
DFS/BFS from 0 trying every landing index; mark visited. Worst case O(n²) edges if every cell can reach many ahead. Recursing without visited can explode.

## Key insight
Track the farthest index reachable so far while scanning left to right. If you ever stand past that farthest, you are stuck. When the scan finishes without getting stuck, the end is reachable—because the farthest always covers a prefix you could have reached step by step.

## Algorithm
1. `reach = 0`.
2. For each index `i` with step `nums[i]`:
   - If `i > reach`, return False.
   - `reach = max(reach, i + step)`.
3. Return True.

## Trace
`nums = [2, 3, 1, 1, 4]`.

| i | step | reach before | reach after |
|---|---|---|---|
| 0 | 2 | 0 | 2 |
| 1 | 3 | 2 | 4 |
| 2 | 1 | 4 | 4 |
| 3 | 1 | 4 | 4 |
| 4 | 4 | 4 | 8 |

Never `i > reach`; True.

`nums = [3, 2, 1, 0, 4]`: at i=3, reach is 3; from 3 you jump 0 so reach stays 3; i=4 > 3 → False.

## Complexity
Single pass O(n) time, O(1) space. Better than explicit BFS queues for this yes/no question. Jump Game II needs a second "end of current jump range" cursor but the same linear scan idea.

## Edge cases
Single element → True. First element 0 and n>1 → False. Zeros in the middle that are still covered by an earlier long jump. Last index 0 is fine (you already arrived).

## Alternatives and trade-offs
DP `can[i]` true if some earlier `can[j]` reaches i—O(n²). BFS from 0. Working backward: last good position starts at n-1; scan left updating when `i + nums[i] >= good`. Same O(n).

## Common bugs
Comparing `reach >= n` too early and skipping the stuck check. Updating reach before checking `i > reach`. Off-by-one thinking you must land exactly on the end (any overshoot is fine).

## Follow-ups
Jump Game II (min jumps). Jump Game III (value as jump both ways). Odd jump / even jump variants.

## Related problems
Jump Game II, Gas Station, Video Stitching, Maximum Jump Length.
