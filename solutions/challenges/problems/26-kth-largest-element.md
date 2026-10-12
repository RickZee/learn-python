# 26. Kth Largest Element — walkthrough

## Recognize it
Return the kth largest value in an unsorted array. Duplicates count as separate occurrences: in `[3,2,3,1,2,4,5,5,6]` with k=4 the answer is 4. Look-alike: kth distinct largest (skip duplicates). Another look-alike: top k frequent (rank by count, not by value).

## Brute force
Sort a copy descending and take index `k-1`, or sort ascending and take index `n-k`. Time O(n log n), space O(n) or O(1) if you may sort in place. Fine for moderate n; timed challenges often want better dependence on k.

## Key insight
You only need the boundary of the k largest values, not a full order. A min-heap of size k stores the k largest seen so far; its root is the smallest among them—exactly the kth largest. Each new value either is ignored (≤ root when heap is full) or replaces the root.

## Algorithm
1. Create an empty min-heap.
2. For each `value` in `nums`: push it; if `len(heap) > k`, pop once.
3. Return `heap[0]`.

Equivalently: push all, then pop until k remain—same asymptotics with larger peak space if you push everything first; the size-cap version keeps space O(k).

## Trace
`nums = [3,2,1,5,6,4]`, `k = 2`.

| value | heap (min on left) | after cap |
|---|---|---|
| 3 | [3] | [3] |
| 2 | [2,3] | [2,3] |
| 1 | [1,3,2] | pop → [2,3] |
| 5 | [2,3,5] | pop → [3,5] |
| 6 | [3,5,6] | pop → [5,6] |
| 4 | [4,6,5] | pop → [5,6] |

Root is 5 = 2nd largest.

## Complexity
Each of n pushes/pops on a heap of size ≤ k is O(log k): O(n log k) time, O(k) space. Full sort is O(n log n)—worse when k ≪ n. Quickselect average O(n) / worst O(n²) is faster in the average case but needs careful in-place partitioning and duplicate handling.

## Edge cases
`k = 1` → maximum. `k = n` → minimum. All equal → that value. Negatives and zeros behave normally in the heap. The prompt usually guarantees 1 ≤ k ≤ n.

## Alternatives and trade-offs
Sorting is clearest. Quickselect is the classic O(n) average answer—mention it, implement heap unless asked for linear average. Max-heap of all elements then pop k times is O(n + k log n) and uses O(n) space. Counting sort works only for tiny value ranges.

## Common bugs
Treating k as 0-based (`k`th means pop until one remains after building max-heap of n—easy off-by-one). Using a max-heap of size k by mistake (that tracks the k smallest). Deduplicating when the problem counts multiplicity. Sorting ascending and returning `nums[k]` instead of `nums[-k]`.

## Follow-ups
Kth largest in a stream (maintain the heap across inserts). Find median (two heaps). K closest points (heap by distance).

## Related problems
Top K Frequent Elements, K Closest Points to Origin, Find Median from Data Stream, Sort Colors (selection ideas).
