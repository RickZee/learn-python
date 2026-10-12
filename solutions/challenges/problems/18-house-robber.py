def rob(nums: list[int]) -> int:
    """You cannot rob two adjacent houses. An empty street is 0.

    Approach: at each house, choose the better of skipping it or taking it.
    Time: O(n)
    Space: O(1)
    Alternative: a table of the best total up to each house.
    Common bugs: robbing two adjacent houses, or dropping the case of an empty street.
    """
    previous, current = 0, 0
    for value in nums:
        previous, current = current, max(current, previous + value)
    return current
