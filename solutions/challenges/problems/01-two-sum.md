# 01. Two Sum — walkthrough

## Recognize it
You need a pair of indexes whose values add to a target, and each value can be remembered as you scan. That is a classic hash-map complement problem. A look-alike that is not this pattern is "all pairs that sum to target" with many answers (then you may sort and use two pointers), or a subarray sum (prefix sums).

## Brute force
Try every pair `(i, j)` with `i < j` and test `nums[i] + nums[j] == target`. That is O(n²) time and O(1) extra memory. With n up to 1e5 it is too slow.

## Key insight
When you stand at index `j` with value `v`, you need an earlier index that stored `target - v`. A dict from value to index answers that in expected O(1).

## Algorithm
1. Create an empty dict `seen`.
2. For each index `i` and value `v`, compute `need = target - v`.
3. If `need` is in `seen`, return `[seen[need], i]` (smaller index first because it was stored earlier).
4. Otherwise store `seen[v] = i`.
5. If the loop ends, return `[]` (no pair).

## Trace
`nums = [2, 7, 11, 15]`, `target = 9`.

| i | v | need | seen before | action |
|---|---|---|---|---|
| 0 | 2 | 7 | {} | store 2→0 |
| 1 | 7 | 2 | {2:0} | hit → return [0,1] |

## Complexity
One pass: O(n) time. The dict holds at most n keys: O(n) space. Better than O(n²) when n is large.

## Edge cases
Single element or empty → no pair (`[]`). Two same values that form the target (`[3,3], 6`) must use two indexes. Negatives are fine because dict keys hash them. Exactly one answer is guaranteed on graded cases, but defensive code may return `[]`.

## Alternatives and trade-offs
Sort a copy of pairs `(value, index)` and move two pointers; restore indexes at the end. That is O(n log n) time and avoids a hash map, but is slower and easier to get wrong with duplicate values. Hashing is the default challenge answer for the O(n) target.

## Common bugs
Returning values instead of indexes. Using the same index twice when `2 * v == target` but the value appears once. Overwriting `seen[v]` before checking the complement when duplicates matter (for this problem, store after the check).

## Follow-ups
Return all pairs. Stream values one at a time. What if many valid pairs exist—does the prompt want any pair or all?

## Related problems
Group Anagrams (hashing for grouping), Longest Substring Without Repeating Characters (window + set), Two Sum II on a sorted array (two pointers).
