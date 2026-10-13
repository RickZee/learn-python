import heapq


def k_smallest(nums: list[int], k: int) -> list[int]:
    """Return the k smallest values, sorted.

    Approach: heapify a copy and pop k times.
    Time: O(n + k log n)
    Space: O(n)
    Alternative: heapq.nsmallest.
    Common bugs: sorting the whole list when k is tiny.
    """
    heap = list(nums)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(k)]


def last_stone(stones: list[int]) -> int:
    """Smash the two heaviest until one or none remain. Return the last weight.

    Approach: a max-heap is a min-heap of negated weights.
    Time: O(n log n)
    Space: O(n)
    Alternative: sort and rescan.
    Common bugs: forgetting to push the difference back.
    """
    heap = [-stone for stone in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0
