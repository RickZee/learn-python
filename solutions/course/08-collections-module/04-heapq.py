import heapq


def smallest(nums: list[int]) -> int:
    return heapq.nsmallest(1, nums)[0]


def k_smallest(nums: list[int], k: int) -> list[int]:
    return heapq.nsmallest(k, nums)


def top_scores(nums: list[int], k: int) -> list[int]:
    return heapq.nlargest(k, nums)
