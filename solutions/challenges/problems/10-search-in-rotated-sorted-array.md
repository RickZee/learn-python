# 10. Search in Rotated Sorted Array — walkthrough

## Recognize it
A sorted array was rotated; find target in O(log n). One half of the mid split is always sorted—search there if the target fits, else the other half. Look-alike: find minimum in rotated array (same structure, different return).

## Brute force
Linear scan O(n).

## Key insight
At mid, either `[left..mid]` or `[mid..right]` is sorted. If the target lies in the sorted half's value range, discard the other half.

## Algorithm
1. While `left <= right`, compute mid.
2. On hit, return mid.
3. If left half sorted (`nums[left] <= nums[mid]`): if target in `[nums[left], nums[mid])`, cut right; else cut left.
4. Else right half sorted: symmetric.
5. Return -1.

## Trace
`[4,5,6,7,0,1,2]`, target 0.

| left | right | mid | sorted half | action |
|---|---|---|---|---|
| 0 | 6 | 3 | left 4..7 | target not in range → left=4 |
| 4 | 6 | 5 | right includes 0 | hit path → index 4 |

## Complexity
O(log n) time, O(1) space.

## Edge cases
No rotation. Target at pivot. Missing target. Single element. Two elements.

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure. Find pivot index first, then binary search one side—two passes, same asymptotics, more code.

## Common bugs
Using `<` instead of `<=` when deciding which half is sorted (equals matter). Searching the unsorted half by accident.

## Follow-ups
With duplicates (harder). Find minimum only.

## Related problems
Find Minimum in Rotated Sorted Array, Binary Search, Search Insert Position.
