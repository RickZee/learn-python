

def total(nums: list[int]) -> int:
    return sum(nums)


def min_subarray(nums: list[int]) -> int:
    best = current = nums[0]
    for value in nums[1:]:
        current = min(value, current + value)
        best = min(best, current)
    return best

def running_sum(nums: list[int]) -> list[int]:
    """Return the prefix sums, including each value.

    Approach: add each value to the previous prefix.
    Time: O(n)
    Space: O(n)
    Alternative: itertools.accumulate.
    Common bugs: forgetting the first value.
    """
    totals = []
    current = 0
    for value in nums:
        current += value
        totals.append(current)
    return totals
