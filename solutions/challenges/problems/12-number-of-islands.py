def num_islands(grid: list[list[str]]) -> int:
    """Count islands of land. Land is "1". Four directions connect it.

    Approach: mark visited land as water, then visit its neighbors.
    Time: O(rows * cols)
    Space: O(rows * cols) for the call stack
    Alternative: the same walk with a queue.
    Common bugs: counting diagonal neighbors, or visiting the same land cell again.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(row: int, col: int) -> None:
        if not (0 <= row < rows and 0 <= col < cols) or grid[row][col] != "1":
            return
        grid[row][col] = "0"
        sink(row + 1, col)
        sink(row - 1, col)
        sink(row, col + 1)
        sink(row, col - 1)

    count = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1":
                count += 1
                sink(row, col)
    return count
