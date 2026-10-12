def find_min(nums: list[int]) -> int:
    """Return the minimum of a rotated sorted array of distinct values.

    Approach: if the middle is above the right end, the minimum is to its right.
    Time: O(log n)
    Space: O(1)
    Alternative: a linear scan.
    Common bugs: comparing with the left end, which fails when the minimum is first.
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
