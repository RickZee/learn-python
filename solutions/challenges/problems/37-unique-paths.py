def unique_paths(m: int, n: int) -> int:
    """Ways to walk an m by n grid moving only right or down.

    Approach: one row. Each cell adds the cell to its left.
    Time: O(m * n)
    Space: O(n)
    Alternative: the binomial coefficient C(m + n - 2, m - 1).
    Common bugs: recursion with no cache, which recounts the same cell.
    """
    row = [1] * n
    for _ in range(1, m):
        for col in range(1, n):
            row[col] += row[col - 1]
    return row[-1]
