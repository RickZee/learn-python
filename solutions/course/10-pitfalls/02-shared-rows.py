def one_row(cols: int) -> list[int]:
    return [0] * cols


def make_grid(rows: int, cols: int) -> list[list[int]]:
    return [[0] * cols for _ in range(rows)]


def blank_grid(rows: int, cols: int) -> list[list]:
    return [[None] * cols for _ in range(rows)]
