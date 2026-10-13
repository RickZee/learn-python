def oranges_rotting(grid: list[list[int]]) -> int:
    """Minutes until every fresh orange rots, or -1.

    Approach: multi-source breadth-first search from every rotten orange.
    Time: O(rows * cols)
    Space: O(rows * cols)
    Alternative: simulate minute by minute with a new grid.
    Common bugs: counting a minute when the last round rots nothing.
    """
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    queue = []
    fresh = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 2:
                queue.append((row, col))
            elif grid[row][col] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        nxt = []
        for row, col in queue:
            for drow, dcol in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nrow, ncol = row + drow, col + dcol
                if 0 <= nrow < rows and 0 <= ncol < cols and grid[nrow][ncol] == 1:
                    grid[nrow][ncol] = 2
                    fresh -= 1
                    nxt.append((nrow, ncol))
        queue = nxt
        if nxt:
            minutes += 1
    return minutes if fresh == 0 else -1
