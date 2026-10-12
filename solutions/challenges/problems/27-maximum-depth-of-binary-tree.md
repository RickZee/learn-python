# 27. Maximum Depth of Binary Tree — walkthrough

## Recognize it
Depth is the number of nodes on the longest root-to-leaf path (sometimes people count edges; this prompt counts nodes). Empty tree → 0. Look-alike: minimum depth (shortest root-to-leaf; beware a null child is not a leaf shortcut). Another look-alike: diameter (longest path between any two nodes, not necessarily through the root).

## Brute force
There is no slower useful brute force than visiting every node once—you must look at each node to know the height. A level-order BFS that counts layers is the iterative counterpart of the recursive definition.

## Key insight
Height of a node is `1 + max(height(left), height(right))`, and height of `None` is 0. That recurrence is both the definition and the algorithm. Recursion expresses it directly; BFS counts how many times the queue drains a full level.

## Algorithm
Recursive:
1. If `root is None`, return 0.
2. Return `1 + max(max_depth(root.left), max_depth(root.right))`.

BFS alternative:
1. If empty, return 0.
2. Queue the root; `depth = 0`.
3. While queue non-empty: process current level size, enqueue children, `depth += 1`.
4. Return `depth`.

## Trace
Tree:
```
    3
   / \
  9  20
    /  \
   15   7
```

| call | left depth | right depth | result |
|---|---|---|---|
| 15, 7 | 0 | 0 | 1 |
| 20 | 1 | 1 | 2 |
| 9 | 0 | 0 | 1 |
| 3 | 1 | 2 | 3 |

Answer 3. BFS levels: `{3}` → `{9,20}` → `{15,7}` → three rounds.

## Complexity
Each node visited once: O(n) time. Recursion depth is the height h, so O(h) stack space (O(n) skewed). BFS uses O(w) queue space for the widest level. Both are linear work; choose recursion for clarity unless the tree may be extremely deep.

## Edge cases
Empty → 0. Single node → 1. Left-only chain of length n → n (and recursion depth n). Right-only chain same. Perfect binary tree of height h → h.

## Alternatives and trade-offs
DFS recursion is shortest. Explicit stack DFS storing depths works without call-stack risk. BFS is natural if you already think in levels (same code shape as level-order traversal). Returning edge-count by mistake (`depth - 1`) fails node-count prompts.

## Common bugs
Counting edges instead of nodes (`return max(...)` without the `+1`, or initializing empty as -1 inconsistently). Treating a node with one null child as depth 0 on that side incorrectly for min-depth (not this problem, but a common mix-up). Not handling `None` root.

## Follow-ups
Minimum depth. Balanced binary tree (height difference ≤ 1). Diameter of binary tree. Max depth of an N-ary tree.

## Related problems
Binary Tree Level Order Traversal, Diameter of Binary Tree, Balanced Binary Tree, Invert Binary Tree.
