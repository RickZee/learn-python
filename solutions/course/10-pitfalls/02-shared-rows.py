def one_row(cols: int) -> list[int]:
    return [0] * cols


def make_grid(rows: int, cols: int) -> list[list[int]]:
    grid = []
    for _ in range(rows):
        row = [0] * cols
        grid.append(row)
    return grid


def blank_grid(rows: int, cols: int) -> list[list]:
    return [[None] * cols for _ in range(rows)]


def board(rows: int, cols: int) -> list[list[int]]:
    grid = []
    for _ in range(rows):
        grid.append([0] * cols)
    return grid
