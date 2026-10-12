def sorted_pair(nums: list[int], target: int) -> tuple[int, int] | None:
    """nums is sorted. Return the two indexes that sum to target, or None.

    Approach: move the left index up when the sum is low, and the right one down.
    Time: O(n)
    Space: O(1)
    Alternative: a hash map, which does not need the list to be sorted.
    """
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def has_pair(nums: list[int], target: int) -> bool:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return True
        if total < target:
            left += 1
        else:
            right -= 1
    return False


def pair_values(nums: list[int], target: int):
    found = sorted_pair(nums, target)
    if found is None:
        return None
    left, right = found
    return (nums[left], nums[right])
