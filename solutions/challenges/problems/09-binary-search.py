def binary_search(nums: list[int], target: int) -> int:
    """Return the index of target, or -1. nums is sorted and has no duplicates.

    Approach: halve the remaining range by comparing the middle value.
    Time: O(log n)
    Space: O(1)
    Alternative: bisect_left, then check that the index holds the target.
    Common bugs: an off-by-one that skips the last index, or a range that never shrinks.
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
