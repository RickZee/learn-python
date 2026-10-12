def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the two indexes, smaller first. One pair. Each index once.

    Approach: one pass, store each value's index, and look for the complement.
    Time: O(n)
    Space: O(n)
    Alternative: sort a copy and move two pointers inward.
    Common bugs: returning the values instead of the indexes, or using one index twice.
    """
    seen = {}
    for index, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], index]
        seen[value] = index
    return []
