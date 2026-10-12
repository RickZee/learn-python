def diameter_of_values(values: list[int | None]) -> int:
    """Longest edge-count path in a binary tree given as level-order values.

    Approach: DFS returns height; at each node update best with left+right.
    Time: O(n)
    Space: O(h) recursion
    Alternative: treat the tree as a graph and run two BFS passes.
    Common bugs: returning height; counting nodes instead of edges.
    """
    n = len(values)
    best = 0

    def depth(i):
        nonlocal best
        if i >= n or values[i] is None:
            return 0
        left = depth(2 * i + 1)
        right = depth(2 * i + 2)
        best = max(best, left + right)
        return 1 + max(left, right)

    depth(0)
    return best
