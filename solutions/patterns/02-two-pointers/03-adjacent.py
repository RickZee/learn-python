def end_area(height: list[int]) -> int:
    width = len(height) - 1
    return min(height[0], height[-1]) * width


def widest(height: list[int]) -> int:
    return end_area(height)


def adjacent_max(nums: list[int]) -> int:
    """Return the largest sum of two neighbors, or 0 when there is no pair.

    Approach: one pass over adjacent pairs.
    Time: O(n)
    Space: O(1)
    Alternative: max of a sliding window of length 2.
    Common bugs: including a single value as a pair.
    """
    if len(nums) < 2:
        return 0
    best = nums[0] + nums[1]
    for index in range(1, len(nums) - 1):
        best = max(best, nums[index] + nums[index + 1])
    return best
