# 14. Merge Two Sorted Lists — walkthrough

## Recognize it
Two singly linked lists are already sorted non-decreasing by value. Produce one sorted list that contains every node from both inputs. Either list may be empty. You may reuse the existing nodes (splice them) rather than copy values. A look-alike is merge k sorted lists (needs a heap or divide-and-conquer). Another is merge sorted arrays, where you write into a buffer from the end instead of threading pointers.

## Brute force
Collect every value from both lists into an array, sort the array, and build a new linked list. Time is O((n+m) log(n+m)) for the sort, plus O(n+m) space for the array and new nodes. That ignores the fact that each input is already sorted, so you pay for order you already have.

## Key insight
Because both lists are sorted, the next node in the merged result is always the smaller of the two current heads. A dummy node gives `tail` a stable place to attach; when one list empties, append the other list's remaining tail in one assignment—no more comparisons needed.

## Algorithm
1. Create `dummy = ListNode()` and set `tail = dummy`.
2. While both `list1` and `list2` are non-empty:
   - If `list1.val <= list2.val`, attach `list1` to `tail.next` and advance `list1`.
   - Otherwise attach `list2` and advance `list2`.
   - Advance `tail` to the node just attached.
3. Set `tail.next` to whichever list is still non-empty (or `None` if both finished together).
4. Return `dummy.next` (the real head). Empty+empty returns `None`.

## Trace
`list1 = 1 → 2 → 4`, `list2 = 1 → 3 → 4`.

| compare | attach | list1 | list2 | merged so far |
|---|---|---|---|---|
| 1 vs 1 | first 1 | 2→4 | 1→3→4 | 1 |
| 2 vs 1 | 1 | 2→4 | 3→4 | 1→1 |
| 2 vs 3 | 2 | 4 | 3→4 | 1→1→2 |
| 4 vs 3 | 3 | 4 | 4 | 1→1→2→3 |
| 4 vs 4 | 4 (list1) | None | 4 | …→4 |
| leftover | attach 4 | — | — | 1→1→2→3→4→4 |

## Complexity
Each node is visited exactly once: O(n+m) time. Only dummy and tail pointers are extra: O(1) space beyond the output, which reuses input nodes. Sorting from scratch would be slower for large n and m.

## Edge cases
One list empty → return the other unchanged. Both empty → `None`. All values in one list smaller than the other → one side drains first, then the leftover attach handles the rest. Duplicate values: use `<=` so ties take from `list1` stably; either tie-break is fine if the prompt does not care.

## Alternatives and trade-offs
Recursion: return the smaller head with `head.next = merge(rest, other)`. Elegant, but O(n+m) stack frames. Building new nodes from values avoids mutating inputs when the caller needs the originals intact—cost is more allocations. For k lists, pairwise merge is O(k·N) or heap merge is O(N log k); this two-list splice is the base case of those designs.

## Common bugs
Forgetting to attach the leftover tail, which silently drops the rest of one list. Advancing `tail` before setting `tail.next`, which loses the chain. Comparing with `<` only and mishandling equals if a grader checks node identity order. Returning `dummy` instead of `dummy.next`, which inserts a bogus zero-value head.

## Follow-ups
Merge k sorted lists. Merge sorted arrays in place. Insert a node into a sorted list. Sort a linked list via merge sort (split, recurse, merge).

## Related problems
Merge Intervals (sorted merge of ranges), Merge k Sorted Lists, Sort List, Add Two Numbers (digit-by-digit list walk).
