def can_jump(nums: list[int]) -> bool:
    """Whether you can reach the last index given jump lengths.

    Approach: scan left to right tracking the farthest reachable index.
    Time: O(n)
    Space: O(1)
    Alternative: BFS/DFS on indexes, or DP can[i].
    Common bugs: updating reach after standing past it; requiring exact landings.
    """
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True
