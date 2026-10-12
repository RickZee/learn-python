# 11. Find Minimum in Rotated Sorted Array — walkthrough

## Recognize it
Rotated sorted distinct values; return the minimum in O(log n). Compare mid to the right end: if mid is greater, the min is to the right; else min is at mid or left. Look-alike: search for a target in the same shape.

## Brute force
`min(nums)` linear scan.

## Key insight
The rotation point is the minimum. When `nums[mid] > nums[right]`, the increasing run continues past mid, so the dip is on the right.

## Algorithm
1. `left, right = 0, n-1`.
2. While `left < right`: mid; if `nums[mid] > nums[right]` then `left = mid+1` else `right = mid`.
3. Return `nums[left]`.

## Trace
`[3,4,5,1,2]`.

| left | right | mid | nums[mid] vs right |
|---|---|---|---|
| 0 | 4 | 2 | 5>2 → left=3 |
| 3 | 4 | 3 | 1<2 → right=3 |
| done | | | nums[3]=1 |

## Complexity
O(log n) time, O(1) space.

## Edge cases
No rotation (already sorted). Two elements. Minimum at index 0. Single element.

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure. Linear min is fine for tiny n. Comparing with left instead of right fails when the array is not rotated.

## Common bugs
Comparing mid to left. Using `<=` incorrectly so the loop does not shrink. Returning the index instead of the value.

## Follow-ups
With duplicates. Also return the rotation count.

## Related problems
Search in Rotated Sorted Array, Binary Search, Peak Element.
