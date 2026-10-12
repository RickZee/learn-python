# 29. Validate Binary Search Tree — walkthrough

## Recognize it
Every node's value must be strictly greater than all values in its left subtree and strictly less than all in its right subtree—not merely greater/less than its parent. Empty tree is valid. Look-alike: checking only parent links (`left.val < node.val < right.val`), which accepts illegal deep violations. Another look-alike: validate a min-heap shape.

## Brute force
For each node, scan its entire left subtree for a max and right for a min and compare—O(n²) on skewed trees. Correct but slow. Better: one inorder walk should produce a strictly increasing sequence.

## Key insight
Each node inherits an open interval `(low, high)` of allowed values from its ancestors. Root starts in `(-∞, +∞)`. Left child must lie in `(low, node.val)`; right child in `(node.val, high)`. If any node falls outside its interval, the tree is not a BST.

## Algorithm
1. Define `walk(node, low, high)`:
   - `None` → True.
   - If not `low < node.val < high`, return False.
   - Return `walk(left, low, node.val) and walk(right, node.val, high)`.
2. Call `walk(root, -inf, +inf)`.

Inorder alternative: traverse left-root-right, ensuring each value `>` previous.

## Trace
Illegal tree:
```
  5
 / \
1   4
   / \
  3   6
```
Node 3 has parent 4, and 3 < 4, but 3 is in the right subtree of 5, so it must be > 5. Bounds at 3: `(5, 4)` which is empty → False.

Legal:
```
  2
 / \
1   3
```
| node | low | high | ok? |
|---|---|---|---|
| 2 | -∞ | ∞ | yes |
| 1 | -∞ | 2 | yes |
| 3 | 2 | ∞ | yes |

## Complexity
One visit per node: O(n) time. Recursion stack O(h). Inorder with a prev pointer is the same asymptotics. The O(n²) per-subtree min/max scans are the approach to avoid.

## Edge cases
Single node → True. Duplicates: strict BST rejects equals (`low < val < high`). Values at int extremes—use unbounded floats/`None` sentinels carefully so `val == INT_MIN` still works. Left child equal to parent → False under strict rules.

## Alternatives and trade-offs
Bounds DFS is easy to explain. Inorder is intuitive if you already know BSTs print sorted. Morris inorder can validate with O(1) extra space by threading—overkill unless asked. Returning early on first failure matters for large invalid trees.

## Common bugs
Only comparing with the parent. Using `<=` / `>=` inconsistently with the prompt's strictness. Reusing the same `low`/`high` for both children. Integer sentinel `low = -2**31` that collides with a real value—prefer open bounds with `None` checks or floats.

## Follow-ups
Recover a BST with two swapped nodes. Kth smallest in a BST (inorder). Trim a BST to a range (same bounds idea).

## Related problems
Kth Smallest in a BST, Lowest Common Ancestor of a BST, Recover Binary Search Tree, Inorder Successor.
