# 52. Kth Smallest in a BST — walkthrough

## Recognize it
BST; return the k-th smallest value (1-indexed). In-order traversal of a BST yields sorted order. Look-alike: kth largest (reverse in-order or k from the end). Another look-alike: kth in an unsorted array (quickselect / heap).

## Brute force
Flatten every value into a list, sort, pick index `k-1`. Correct even if the tree were not a BST, but wastes the ordering and uses O(n) time and space always.

## Key insight
In-order walk visits values ascending. Stop after k visits. With Node pointers you can recurse left, visit, recurse right and decrement k. This repo's harness passes a level-order list (with `None` holes); collecting non-`None` values and sorting matches the BST in-order multiset for the graded trees (unique values).

## Algorithm
Reference solution used here:

1. `values = [v for v in level if v is not None]`.
2. `values.sort()`.
3. Return `values[k - 1]`.

Node-pointer version:

1. Iterative stack in-order; each pop is the next smallest; after k pops, return that value.

## Trace
Level order `[3,1,4,None,2]`, `k = 1`.

Non-null values `[3,1,4,2]` → sorted `[1,2,3,4]` → answer `1`.

In-order Node walk: visit 1 first → return 1 for k=1. For k=3 visit 1,2,3 → return 3.

| k | in-order position | value |
|---|---|---|
| 1 | first | 1 |
| 2 | second | 2 |
| 3 | third | 3 |

## Complexity
List+sort: O(n log n) time, O(n) space—acceptable for small challenge trees and this stub. True in-order early stop: O(h + k) time, O(h) space. Augmenting nodes with subtree sizes gives O(h) per query after O(n) build.

## Edge cases
`k = 1` (minimum). `k = n` (maximum). Skewed tree (stack depth n). Duplicates if allowed—define stable k. Empty children as `None` in level order must be skipped, not treated as 0.

## Alternatives and trade-offs
Morris in-order for O(1) extra space. Subtree counts for repeated queries. Prefer stack in-order in timed challenges to show you use BST structure; mention sort-of-values only as a fallback when the API is a flat list.

## Common bugs
Off-by-one (`k` vs `k-1`). Pre-order or level-order instead of in-order. Counting `None` placeholders as values. Mutating the tree while traversing.

## Follow-ups
Kth largest. Closest BST value. BST iterator (`next` in amortized O(1)).

## Related problems
Binary Tree Inorder Traversal, Validate BST, Lowest Common Ancestor of BST, Delete Node in a BST.
