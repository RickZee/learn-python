def is_rotated(nums: list[int]) -> bool:
    if len(nums) < 2:
        return False
    return nums[0] > nums[-1]


def rotation_index(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return left


def min_index(nums: list[int]) -> int:
    """Return the index of the minimum in a rotated sorted list of distinct values.

    Approach: if the middle is above the right end, the minimum is to its right.
    Time: O(log n)
    Space: O(1)
    Alternative: a linear scan.
    Common bugs: returning the value instead of the index.
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return left
