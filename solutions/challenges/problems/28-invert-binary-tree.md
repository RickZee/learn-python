# 28. Invert Binary Tree — walkthrough

## Recognize it
Swap every left and right child throughout the tree (mirror image). Return the root. Empty tree stays empty. Look-alike: swap only children of one node. Another look-alike: reverse a linked list (linear structure; here every node swaps its pair of children).

## Brute force
You still visit every node once—there is no asymptotic brute that is worse in a useful way. Building a new tree from a level-order listing reversed per level works but allocates new nodes unnecessarily when in-place swaps are allowed.

## Key insight
Mirroring is recursive: invert the left subtree, invert the right subtree, then swap the two child pointers on the current node—or swap first and then invert the (new) children. Either order works if you invert both sides after the swap of references. The clean one-liner swaps while assigning the recursive results.

## Algorithm
1. If `root is None`, return `None`.
2. Set `root.left, root.right = invert_tree(root.right), invert_tree(root.left)`.
3. Return `root`.

BFS/queue version: enqueue root; while queue: pop, swap its children, enqueue non-null children.

## Trace
```
    4
   / \
  2   7
 / \ / \
1  3 6  9
```

After invert:
```
    4
   / \
  7   2
 / \ / \
9  6 3  1
```

Step at node 2: children 1 and 3 swap to 3 and 1; same idea at 7 and at root (2↔7).

## Complexity
O(n) time—every node swapped once. O(h) recursion stack or O(w) queue space. Creating a fresh mirrored tree is also O(n) time and O(n) space for new nodes.

## Edge cases
Empty → `None`. Single node → itself. Left-only chain becomes right-only. Already symmetric trees look unchanged in shape but child pointers were still swapped (idempotent only after two inverts).

## Alternatives and trade-offs
Recursion is the usual default. Iterative BFS avoids deep recursion on skewed trees. Post-order "invert children then swap" vs swap-then-recurse are equivalent if both children are processed; the bug is inverting the same original child twice by swapping after both recursive calls on the pre-swap pointers without care.

## Common bugs
Writing `invert_tree(root.left); invert_tree(root.right);` then swapping—usually fine—but `root.left = invert_tree(root.left)` after already swapping can invert one side twice. Forgetting to return the root. Swapping values instead of child pointers when values are not unique.

## Follow-ups
Check if two trees are mirrors. Symmetric tree (is tree equal to its invert). Invert only nodes at odd depths.

## Related problems
Symmetric Tree, Maximum Depth of Binary Tree, Binary Tree Level Order Traversal, Reverse Linked List.
