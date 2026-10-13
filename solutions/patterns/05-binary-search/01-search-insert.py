def contains(nums: list[int], target: int) -> bool:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return True
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


def first_at_least(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    answer = -1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            answer = mid
            right = mid - 1
        else:
            left = mid + 1
    return answer


def search_insert(nums: list[int], target: int) -> int:
    """Return the index of target, or the index where it should be inserted.

    Approach: binary search for the first value that is not smaller than target.
    Time: O(log n)
    Space: O(1)
    Alternative: bisect_left.
    Common bugs: returning -1 when the target is missing.
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
