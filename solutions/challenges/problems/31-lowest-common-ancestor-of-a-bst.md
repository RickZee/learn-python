# 31. Lowest Common Ancestor of a BST — walkthrough

## Recognize it
In a binary search tree, find the lowest common ancestor of two values p and q—the deepest node that has both as descendants (a node may be an ancestor of itself). The solution here returns the ancestor's value. Look-alike: LCA in a general binary tree (no ordering; need parent pointers or a post-order walk). Another look-alike: find distance between two nodes.

## Brute force
Walk from root to p recording the path, same for q, then last common node on the two paths. Time O(h) with O(h) space for paths—fine, but the BST property lets you decide the branch with only the current node and no stored paths.

## Key insight
If both p and q are less than the current value, the LCA is in the left subtree. If both are greater, go right. Otherwise the current node sits between them (or equals one of them)—that split point is the LCA. One downward walk suffices.

## Algorithm
1. Start at `node = root`.
2. While `node` is not `None`:
   - If `p < node.val` and `q < node.val`, go left.
   - Else if `p > node.val` and `q > node.val`, go right.
   - Else return `node.val` (split or match).
3. If the loop exits, the values were not in the tree (raise or return a sentinel per prompt).

## Trace
BST:
```
      6
     / \
    2   8
   / \ / \
  0  4 7  9
    / \
   3   5
```
p=2, q=8 → at 6, one side left one side right → LCA value 6.

p=2, q=4 → at 6 both < 6 → go left to 2; at 2, p equals node and q > 2 → return 2 (ancestor of itself).

| p,q | node | decision |
|---|---|---|
| 2,8 | 6 | split → 6 |
| 2,4 | 6 | both left |
| 2,4 | 2 | split/match → 2 |

## Complexity
One path toward a leaf: O(h) time, O(1) extra space iteratively. Path-pair method is O(h) time and O(h) space. General-tree LCA is O(n) without preprocessing.

## Edge cases
One value is the ancestor of the other—return the ancestor. p and q unordered relative to each other—compare both against node without assuming `p < q` (or sort them first). Duplicates usually absent in BST LCA prompts. Missing values: this code raises if you walk off the tree.

## Alternatives and trade-offs
Recursive form mirrors the same three-way branch. Parent-pointer climb works for general trees. For binary trees without BST order, recurse: if left and right each report a find, root is LCA. Prefer the BST walk when ordering is guaranteed—it is shorter and O(h).

## Common bugs
Returning as soon as you match one of p or q without checking whether the other still lies below (actually the split rule handles "node equals p" correctly—bugs come from requiring both children to be non-null). Assuming `p < q` and writing only one comparison. Using a general-tree post-order and getting O(n) when O(h) was available.

## Follow-ups
LCA of a binary tree (no BST). LCA with parent pointers. Kth ancestor queries with binary lifting.

## Related problems
Validate Binary Search Tree, Kth Smallest in a BST, Lowest Common Ancestor of a Binary Tree, Delete Node in a BST.
