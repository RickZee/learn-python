
def find_kth_largest(nums: list[int], k: int) -> int:
    """The kth largest value, counting duplicates.

    Approach: a min-heap of the k largest values.
    Time: O(n log k)
    Space: O(k)
    Alternative: sort a copy and index from the end.
    Common bugs: treating k as 0-based, or skipping duplicates.
    """
    import heapq

    heap: list[int] = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
