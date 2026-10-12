def max_window_sum(nums: list[int], k: int) -> int:
    """Return the largest sum of any k consecutive values.

    Approach: add the value that enters and drop the value that leaves.
    Time: O(n)
    Space: O(1)
    Alternative: recompute the sum of each window.
    """
    window = sum(nums[:k])
    best = window
    for index in range(k, len(nums)):
        window += nums[index] - nums[index - k]
        best = max(best, window)
    return best


def first_window(nums: list[int], k: int) -> int:
    return sum(nums[:k])


def min_window_sum(nums: list[int], k: int) -> int:
    window = sum(nums[:k])
    best = window
    for index in range(k, len(nums)):
        window += nums[index] - nums[index - k]
        best = min(best, window)
    return best
