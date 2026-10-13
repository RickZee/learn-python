def end_profit(prices: list[int]) -> int:
    if len(prices) < 2:
        return 0
    return max(0, prices[-1] - prices[0])


def up_days(prices: list[int]) -> int:
    return sum(prices[index] > prices[index - 1] for index in range(1, len(prices)))


def pivot_index(nums: list[int]) -> int:
    """Return an index whose left sum equals its right sum, or -1.

    Approach: total minus the running left sum is the right sum.
    Time: O(n)
    Space: O(1)
    Alternative: an explicit prefix array.
    Common bugs: including the pivot value in both sides.
    """
    total = sum(nums)
    left = 0
    for index, value in enumerate(nums):
        if left == total - left - value:
            return index
        left += value
    return -1
