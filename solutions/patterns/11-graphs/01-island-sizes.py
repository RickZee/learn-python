

def cell_count(grid: list[list[str]]) -> int:
    return sum(cell == "1" for row in grid for cell in row)


def largest_island(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    grid = [row[:] for row in grid]

    def measure(row: int, col: int) -> int:
        if not (0 <= row < rows and 0 <= col < cols) or grid[row][col] != "1":
            return 0
        grid[row][col] = "0"
        return (
            1
            + measure(row + 1, col)
            + measure(row - 1, col)
            + measure(row, col + 1)
            + measure(row, col - 1)
        )

    best = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1":
                best = max(best, measure(row, col))
    return best

def island_sizes(grid: list[list[str]]) -> list[int]:
    """Return the sizes of the islands, sorted. Land is "1".

    Approach: sink each island while counting its cells.
    Time: O(rows * cols)
    Space: O(rows * cols) for the call stack
    Alternative: the same walk with a queue.
    Common bugs: counting a corner as connected.
    """
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    grid = [row[:] for row in grid]

    def measure(row: int, col: int) -> int:
        if not (0 <= row < rows and 0 <= col < cols) or grid[row][col] != "1":
            return 0
        grid[row][col] = "0"
        return (
            1
            + measure(row + 1, col)
            + measure(row - 1, col)
            + measure(row, col + 1)
            + measure(row, col - 1)
        )

    sizes = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1":
                sizes.append(measure(row, col))
    return sorted(sizes)
