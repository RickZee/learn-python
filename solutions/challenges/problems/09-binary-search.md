# 09. Binary Search — walkthrough

## Recognize it
Sorted array, find target index or report missing. Halve the range each step. Look-alike: search in rotated array (still binary, but half-sorted logic).

## Brute force
Linear scan: O(n).

## Key insight
Compare the middle value to the target; discard the half that cannot contain it. Loop while `left <= right`.

## Algorithm
1. `left, right = 0, n-1`.
2. While `left <= right`: `mid = (left+right)//2`; return mid on hit; move left or right.
3. Return `-1`.

## Trace
`nums=[-1,0,3,5,9,12]`, target 9.

| left | right | mid | nums[mid] |
|---|---|---|---|
| 0 | 5 | 2 | 3 → left=3 |
| 3 | 5 | 4 | 9 → hit |

## Complexity
O(log n) time, O(1) space.

## Edge cases
Empty array. Target below min or above max. Single element. Target at ends.

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure. `bisect_left` then equality check. Recursive binary search uses stack space.

## Common bugs
`left < right` without careful mid update infinite loops. Overflow-style mid in other languages (not Python). Off-by-one on right.

## Follow-ups
First/last position of target. Search insert position. Rotated search.

## Related problems
Search Insert Position, Find Minimum in Rotated Sorted Array, Koko Eating Bananas (answer-space binary search).
