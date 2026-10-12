def max_subarray(nums: list[int]) -> int:
    """Return the largest sum of a contiguous subarray.

    Approach: extend the current run, or start over when the run is a loss.
    Time: O(n)
    Space: O(1)
    Alternative: a prefix-sum scan of every pair of ends.
    Common bugs: resetting at zero, which drops an array of only negative values.
    """
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best
