import heapq


def smallest(nums: list[int]) -> int:
    return heapq.nsmallest(1, nums)[0]


def k_smallest(nums: list[int], k: int) -> list[int]:
    heap = list(nums)
    heapq.heapify(heap)
    result = heapq.nsmallest(k, nums)
    return result


def three_smallest(nums: list[int]) -> list[int]:
    return heapq.nsmallest(3, nums)


def top_scores(nums: list[int], k: int) -> list[int]:
    return heapq.nlargest(k, nums)
