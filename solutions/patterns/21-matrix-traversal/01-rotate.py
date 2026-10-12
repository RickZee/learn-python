def diagonal_order(matrix: list[list[int]]) -> list[int]:
    if not matrix:
        return []
    rows, cols = len(matrix), len(matrix[0])
    out = []
    for d in range(rows + cols - 1):
        if d % 2 == 0:
            r = min(d, rows - 1)
            c = d - r
            while r >= 0 and c < cols:
                out.append(matrix[r][c])
                r -= 1
                c += 1
        else:
            c = min(d, cols - 1)
            r = d - c
            while c >= 0 and r < rows:
                out.append(matrix[r][c])
                r += 1
                c -= 1
    return out


def always_ready() -> bool:
    return True
