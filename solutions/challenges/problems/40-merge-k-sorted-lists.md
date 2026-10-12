# 40. Merge K Sorted Lists — walkthrough

## Recognize it
You are given `k` sorted linked lists; merge them into one sorted list. Look-alike: merge two sorted lists (same idea, no heap). Another look-alike: merge k sorted arrays (same heap pattern with indexes).

## Brute force
Collect every value into an array, sort, rebuild a list: O(n log n) for n total nodes, and you ignore that each list is already sorted. Repeatedly merge list 1 with list 2, then with list 3, … is O(k·n) comparisons if done naively one node at a time across growing results.

## Key insight
At every moment the next global minimum is among the current heads of the k lists. A min-heap of those heads gives the smallest in O(log k). After you take a node, push its successor from the same list. Tie-break heap entries with a unique index so nodes need not be comparable.

## Algorithm
1. Push `(node.val, list_index, node)` for each non-empty list head.
2. Dummy `tail`; while the heap is non-empty:
   - Pop the smallest; append that node to `tail`.
   - If `node.next` exists, push `(node.next.val, list_index, node.next)`.
3. Return `dummy.next`.

## Trace
Lists: `1→4→5`, `1→3→4`, `2→6`.

| pop | heap heads (vals) after | output so far |
|---|---|---|
| 1 (list0) | 4,1,2 | 1 |
| 1 (list1) | 4,3,2 | 1→1 |
| 2 (list2) | 4,3,6 | 1→1→2 |
| 3 | 4,4,6 | …→3 |
| 4 (list0) | 5,4,6 | …→4 |
| 4 (list1) | 5,6 | …→4 |
| 5 | 6 | …→5 |
| 6 | empty | …→6 |

## Complexity
Each of n nodes is pushed and popped once: O(n log k) time. Heap holds at most k entries: O(k) extra space (output reuses input nodes). Pairwise merge (divide and conquer) is also O(n log k) and can be nicer without a heap library.

## Edge cases
`lists` empty or all `None` → `None`. Single list → return it unchanged. One-node lists. Duplicate values across lists—stable order among equals does not matter for correctness here. Very large k with tiny lists vs small k with long lists—heap still wins.

## Alternatives and trade-offs
Divide-and-conquer: merge pairs until one list remains—same asymptotics, no heap tuples. Tournament trees are overkill. Sorting all values is fine for tiny n in production scripts, not the challenge target.

## Common bugs
Pushing `ListNode` into the heap without a tie-breaker so Python 3 compares nodes and crashes. Forgetting to push `node.next`. Losing the head by not using a dummy. Mutating `lists` indexes incorrectly when a list empties.

## Follow-ups
Merge k sorted arrays. Smallest range covering elements from each list. External sort with k-way merge.

## Related problems
Merge Two Sorted Lists, Sort List, Find K Pairs with Smallest Sums, Kth Smallest in Sorted Matrix.
