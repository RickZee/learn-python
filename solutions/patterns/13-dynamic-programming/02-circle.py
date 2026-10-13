def best_end(nums: list[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(nums[0], nums[-1])


def rob_even(nums: list[int]) -> int:
    return sum(nums[::2])


def rob_circle(nums: list[int]) -> int:
    """Rob a circle of houses. The first and last are adjacent.

    Approach: the better of robbing the line without the last house, or without the first.
    Time: O(n)
    Space: O(1)
    Alternative: the same recurrence with a table.
    Common bugs: robbing both ends.
    """

    def line(houses: list[int]) -> int:
        skip = take = 0
        for value in houses:
            skip, take = take, max(take, skip + value)
        return take

    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(line(nums[:-1]), line(nums[1:]))
