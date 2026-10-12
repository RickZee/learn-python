# 56. Remove Nth Node From End of List — walkthrough

## Recognize it
Singly linked list; delete the n-th node counting from the end in one pass. Look-alike: remove duplicates / remove value (different scan). Another look-alike: rotate list (also two pointers with a gap).

## Brute force
Walk once for length L, then walk `L-n` from the head to delete—two passes. Fine for timed challenges if allowed; one-pass is the usual follow-up.

## Key insight
Keep a gap of `n+1` links between `fast` and `slow` starting from a dummy before the head. When `fast` hits the end, `slow` sits just before the victim, so `slow.next = slow.next.next`. Dummy covers deleting the original head.

## Algorithm
(This repo uses a value list; indexes mirror the pointer idea.)

1. `dummy = [0] + values`; `fast = slow = 0`.
2. Advance `fast` by `n+1`.
3. While `fast < len(dummy)`: advance both.
4. `del dummy[slow+1]`; return `dummy[1:]`.

Node version: same with `fast = slow = dummy`, move fast n+1 steps, then move both until fast is None.

## Trace
`values = [1,2,3,4,5]`, `n = 2` (remove 4).

| step | fast | slow | note |
|---|---|---|---|
| after +3 | 3 | 0 | gap n+1 |
| walk | 4 | 1 | |
| walk | 5 | 2 | |
| walk | 6=end | 3 | slow before 4 |

Delete index 4 in dummy → `[1,2,3,5]`.

## Complexity
O(L) time, O(1) extra pointers (value-list form uses O(L) for the copy). Two-pass length method is the same asymptotics with clearer code.

## Edge cases
Remove the head (`n = length`). Remove the tail (`n = 1`). Single-node list. `n` equal to length with dummy—slow stays at dummy. Off-by-one advancing only `n` instead of `n+1`.

## Alternatives and trade-offs
Two-pass is acceptable unless the prompt forbids it. Recursing to the end and deleting on the way back uses O(L) stack. Prefer dummy + gap in timed challenges to show one-pass skill.

## Common bugs
Gap of `n` instead of `n+1` so you delete the wrong node. No dummy when deleting the head. Losing the list by returning `slow.next` incorrectly. Using 0-based n.

## Follow-ups
Remove every n-th node in a circle (Josephus). Swap nodes in pairs. Reverse nodes in k-group.

## Related problems
Middle of the Linked List, Rotate List, Swap Nodes in Pairs, Delete Node in a Linked List.
