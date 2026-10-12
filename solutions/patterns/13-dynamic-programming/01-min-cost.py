

def small(n: int) -> int:
    if n <= 2:
        return n
    return n


def climb_three(n: int) -> int:
    if n <= 2:
        return n
    one, two, three = 1, 2, 4
    for _ in range(4, n + 1):
        one, two, three = two, three, one + two + three
    return three

def min_cost(cost: list[int]) -> int:
    """Minimum cost to reach the top. You may start on step 0 or 1, and climb 1 or 2 steps.

    Approach: the cost to leave step i is cost[i] plus the cheaper of the next two steps.
    Time: O(n)
    Space: O(1)
    Alternative: a full table.
    Common bugs: charging a cost for the top itself.
    """
    one = two = 0
    for value in reversed(cost):
        one, two = value + min(one, two), one
    return min(one, two)
