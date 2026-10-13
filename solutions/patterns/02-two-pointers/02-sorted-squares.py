def zero_pairs(nums: list[int]) -> int:
    ordered = sorted(nums)
    count = 0
    left, right = 0, len(ordered) - 1
    while left < right:
        total = ordered[left] + ordered[right]
        if total == 0:
            count += 1
            left += 1
            right -= 1
        elif total < 0:
            left += 1
        else:
            right -= 1
    return count


def sorted_squares(nums: list[int]) -> list[int]:
    """Return the squares of a sorted list, still sorted.

    Approach: two pointers at the ends, write the larger square from the back.
    Time: O(n)
    Space: O(n) for the answer
    Alternative: square then sort.
    Common bugs: sorting the squares with a comparison that is not needed.
    """
    answer = [0] * len(nums)
    left, right = 0, len(nums) - 1
    for index in range(len(nums) - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            answer[index] = nums[left] * nums[left]
            left += 1
        else:
            answer[index] = nums[right] * nums[right]
            right -= 1
    return answer


def has_triplet(nums: list[int]) -> bool:
    return len(nums) >= 3
