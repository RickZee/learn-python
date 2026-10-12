# 30. Binary Tree Level Order Traversal — walkthrough

## Recognize it
Return values grouped by depth: a list of levels, each level left-to-right. Empty tree → `[]`. Look-alike: zigzag level order (alternate reversing). Another look-alike: flatten to a single BFS list without grouping.

## Brute force
DFS recording `(depth, value)` pairs, then bucket by depth—works in O(n) after sorting by depth if you do not append in order. Unnecessary bookkeeping compared with BFS where the queue already is one level.

## Key insight
At the start of each loop iteration, the queue holds exactly the nodes of the current level. Snapshot their values, then replace the queue with all of their children. That naturally groups levels without storing depths explicitly.

## Algorithm
1. If `root is None`, return `[]`.
2. `levels = []`, `queue = [root]`.
3. While `queue` is non-empty:
   - Append `[node.val for node in queue]` to `levels`.
   - Set `queue = [child for node in queue for child in (node.left, node.right) if child]`.
4. Return `levels`.

## Trace
```
    3
   / \
  9  20
    /  \
   15   7
```

| round | queue nodes | level values | next queue |
|---|---|---|---|
| 1 | 3 | [3] | 9, 20 |
| 2 | 9, 20 | [9, 20] | 15, 7 |
| 3 | 15, 7 | [15, 7] | empty |

Answer `[[3],[9,20],[15,7]]`.

## Complexity
Each node enqueued once: O(n) time. Queue holds a level of width w: O(n) space worst case (complete tree last level ~ n/2). DFS + buckets is also O(n) time and O(n) space for the answer.

## Edge cases
Empty → `[]`. Single node → `[[val]]`. Left-skewed chain → one value per level. Missing children skipped when building the next queue—do not insert placeholders unless the prompt wants a perfect-tree layout.

## Alternatives and trade-offs
Classic `for _ in range(len(queue))` BFS mutates one deque in place—same idea. DFS with `levels[depth].append(val)` is fine and sometimes shorter recursively. Zigzag adds a reverse on odd depths; do not reverse in the basic problem.

## Common bugs
Mixing the next level into the list you are still iterating (mutating the same list while reading). Using a single flat BFS list when the grader expects nested levels. Forgetting the empty-root case and returning `[[]]`. Enqueuing `None` children and then calling `.val` on them.

## Follow-ups
Zigzag level order. Level-order bottom-up (reverse the levels list). Average of levels. Connect next-right pointers.

## Related problems
Binary Tree Zigzag Level Order, Average of Levels, Maximum Depth (count levels), Rotting Oranges (multi-source BFS layers).
