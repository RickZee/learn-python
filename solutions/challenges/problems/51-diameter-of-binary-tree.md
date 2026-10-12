# 51. Diameter of Binary Tree — walkthrough

## Recognize it
Diameter = number of edges on the longest path between any two nodes (path may or may not through the root). Look-alike: maximum depth (one root-to-leaf). Another look-alike: binary tree maximum path sum (node values, can skip a child).

## Brute force
For every node, compute left height + right height as a candidate, and also recurse into children for their diameters—without sharing height work this recomputes heights and can approach O(n²).

## Key insight
One DFS returns the height of a subtree and, as a side effect, updates a global best with `left_height + right_height` (edges through this node). Height is `1 + max(left, right)` for nodes, `0` for null. The best over all nodes is the diameter.

## Algorithm
(This repo uses a level-order `values` list with `None` holes; children of `i` are `2i+1` and `2i+2`.)

1. `best = 0`.
2. `depth(i)`: if out of range or `None`, return 0; else `left = depth(2i+1)`, `right = depth(2i+2)`; `best = max(best, left+right)`; return `1 + max(left, right)`.
3. Call `depth(0)`; return `best`.

## Trace
Tree `[1,2,3,4,5]` (1 with children 2,3; 2 with 4,5).

| node | left h | right h | candidate | height returned |
|---|---|---|---|---|
| 4 | 0 | 0 | 0 | 1 |
| 5 | 0 | 0 | 0 | 1 |
| 2 | 1 | 1 | 2 | 2 |
| 3 | 0 | 0 | 0 | 1 |
| 1 | 2 | 1 | 3 | 3 |

`best` becomes 3 (path 4-2-5 is 2; path 4-2-1-3 is 3).

## Complexity
Each node visited once: O(n) time. Recursion stack O(h). Storing heights in an array is the same asymptotics with explicit space.

## Edge cases
Empty tree → 0. Single node → 0. Skewed chain of n nodes → diameter n-1. Diameter entirely in the left subtree (root not on the path)—the global `best` still catches it at the subtree root.

## Alternatives and trade-offs
Two BFS (farthest from an arbitrary node, then farthest from that)—works on trees as graphs. Post-order with Node objects is the usual challenge form; the index form here matches the notebook harness.

## Common bugs
Returning height instead of diameter. Counting nodes instead of edges (`left+right+1`). Not updating `best` at every node. Treating `None` holes as zeros incorrectly in a compact list without holes.

## Follow-ups
Diameter of an N-ary tree. Longest univalue path. Maximum path sum.

## Related problems
Maximum Depth of Binary Tree, Binary Tree Maximum Path Sum, Longest Univalue Path, Diameter of N-Ary Tree.
