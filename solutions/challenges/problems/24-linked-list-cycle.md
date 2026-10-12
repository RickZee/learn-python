# 24. Linked List Cycle — walkthrough

## Recognize it
Decide whether a singly linked list contains a cycle: some node's `next` eventually points back to an earlier node. Return True or False. You typically may not mutate the list structure in a destructive way that the grader forbids; read-only traversal is preferred. Look-alike: find the node where the cycle begins (Floyd phase 2). Another look-alike: detect a cycle in a directed graph (colors / DFS stack), which needs adjacency lists instead of a single `next` chain.

## Brute force
Walk from the head, storing every seen node id in a set. If you meet a node already in the set, there is a cycle. If you hit `None`, there is not. Time O(n), space O(n). Correct and simple; timed challenges often ask for O(1) extra memory next.

## Key insight
Floyd's tortoise and hare: move `slow` one step and `fast` two steps. In a finite list without a cycle, `fast` hits `None`. In a cycle, `fast` laps `slow` inside the loop and they land on the same node. Meeting proves a cycle; exhausting `fast` proves none. No set required.

## Algorithm
1. Set `slow = fast = head`.
2. While `fast` is not `None` and `fast.next` is not `None`:
   - `slow = slow.next`
   - `fast = fast.next.next`
   - If `slow is fast`, return `True`.
3. Return `False`.

## Trace
List `1 → 2 → 3 → 4 → 2` (cycle back to 2).

| step | slow | fast | meet? |
|---|---|---|---|
| 0 | 1 | 1 | — |
| 1 | 2 | 3 | no |
| 2 | 3 | 2 | no |
| 3 | 4 | 4 | yes → True |

Acyclic `1 → 2 → 3 → None`: after step 1, slow=2, fast=3; next iteration fast moves to `None` via `3.next` and the loop ends → False.

## Complexity
At most a linear number of steps relative to the list length (inside a cycle the gap closes by one each iteration): O(n) time. Only two pointers: O(1) space. The set approach is O(n) time and O(n) space—use it when you need simplicity or must mark nodes anyway.

## Edge cases
Empty list → False. Single node with `next is None` → False. Single node pointing to itself → True (fast and slow meet after one iteration if you move before checking carefully—with the loop above, after first move both sit on that node). Cycle at the head vs cycle deep in the tail—both detected. Two-node mutual cycle.

## Alternatives and trade-offs
Hash set of nodes is clearest. Destroying `next` pointers as you walk can mark visited nodes but mutates input—usually disallowed. Floyd is the standard O(1)-space answer. After detecting a cycle, reset one pointer to head and advance both one step at a time to find the entrance—same toolkit, second phase.

## Common bugs
Moving `fast` without checking `fast.next` first → attribute error on `None`. Comparing values instead of node identity when duplicates values exist. Starting the loop with a move that skips the self-loop edge case if structured wrong. Using `slow == fast` only at the start before any moves and wrongly returning True on a non-empty list—always move before the equality check inside the loop (as written).

## Follow-ups
Linked List Cycle II (return entrance node). Find the length of the cycle. Happy Number (cycle in a functional graph with Floyd). Copy list with random pointer (different structure).

## Related problems
Linked List Cycle II, Middle of the Linked List (fast/slow), Happy Number, Find the Duplicate Number (Floyd on index graph).
