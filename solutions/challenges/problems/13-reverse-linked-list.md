# 13. Reverse Linked List — walkthrough

## Recognize it
You are given the head of a singly linked list and must reverse the direction of every `next` pointer, then return the new head (the old tail). Empty input stays empty; a one-node list is already reversed. A look-alike is "reverse nodes in k-group," which reverses only fixed-size blocks and leaves the remainder alone. Another look-alike is reversing a sublist between two indexes—same pointer flips, but only inside a window.

## Brute force
Walk the list once, push every value onto an array, then build a new list from the array in reverse order. That is correct and easy to reason about: O(n) time and O(n) extra memory for the array (plus another O(n) if you allocate new nodes). It fails the usual challenge space target when the prompt asks for in-place O(1) extra space, and it also rebuilds nodes when you only needed to rewire pointers.

## Key insight
At every node you only need three references: the node you already reversed (`previous`), the node you are flipping (`head`), and the node you have not touched yet (`nxt`). Flip `head.next` to point at `previous`, then slide all three one step forward. When `head` becomes `None`, `previous` is the new head.

## Algorithm
1. Set `previous = None`. The current cursor starts at the given `head`.
2. While the cursor is not `None`:
   - Save `nxt = head.next` so the rest of the list is not lost.
   - Set `head.next = previous` (the actual reverse step).
   - Move `previous = head`, then `head = nxt`.
3. Return `previous`. If the list was empty, the loop never ran and you return `None`.

## Trace
List `1 → 2 → 3 → None`.

| step | head | previous | nxt | list shape after flip |
|---|---|---|---|---|
| start | 1 | None | — | 1→2→3 |
| 1 | 1 | None | 2 | 1→None; rest 2→3 |
| 2 | 2 | 1 | 3 | 2→1→None; rest 3 |
| 3 | 3 | 2 | None | 3→2→1→None |
| done | None | 3 | — | return 3 |

## Complexity
One pass over n nodes: O(n) time. Only a handful of pointers: O(1) extra space. The recursive alternative still visits every node once, so time stays O(n), but the call stack holds n frames and uses O(n) space—worse when the list is long.

## Edge cases
Empty list → return `None`. Single node → return that node unchanged. Two nodes → swap once. Very long lists favor the iterative form so you do not blow the recursion limit. The problem usually allows mutating the given nodes; do not assume you may allocate a fresh list unless the prompt says so.

## Alternatives and trade-offs
Recursion: reverse the suffix first, then set `head.next.next = head` and `head.next = None`. Clear conceptually, but O(n) stack space and harder to debug mid-call. Copy-to-array then rebuild: simplest to write in a rush, wastes memory. Prefer iterative in-place rewiring for the standard O(1)-space ask.

## Common bugs
Forgetting to save `nxt` before overwriting `head.next`, which orphans the rest of the list. Returning `head` (always `None` at the end) instead of `previous`. Using recursion without a base case for `None` or a one-node list. Flipping links but leaving the old head still pointing forward, creating a tiny cycle of length 1.

## Follow-ups
Reverse only the segment between left and right indexes. Reverse in groups of k. Reverse a doubly linked list (also rewire `prev`). Detect a palindrome by reversing the second half in place and comparing.

## Related problems
Merge Two Sorted Lists (pointer surgery on lists), Linked List Cycle (two pointers without reversing), Reorder List (split, reverse half, merge), Swap Nodes in Pairs.
