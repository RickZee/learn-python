def climb_stairs(n: int) -> int:
    """Each step climbs 1 or 2 stairs. Return how many ways there are.

    Approach: the ways to reach n are the ways to reach n-1 plus n-2.
    Time: O(n)
    Space: O(1)
    Alternative: a full table, or recursion with a cache.
    Common bugs: recursion without a cache, which repeats the same stair.
    """
    if n <= 2:
        return n
    previous, current = 1, 2
    for _ in range(3, n + 1):
        previous, current = current, previous + current
    return current
