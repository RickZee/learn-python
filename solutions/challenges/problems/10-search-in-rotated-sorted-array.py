def search_rotated(nums: list[int], target: int) -> int:
    """Return the index of target in a rotated sorted array, or -1.

    Approach: one half is always sorted. Keep the half that can hold the target.
    Time: O(log n)
    Space: O(1)
    Alternative: find the pivot, then binary-search the matching side.
    Common bugs: calling an equal middle unsorted, or searching the wrong half.
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
    return -1
