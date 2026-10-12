def spiral_order(matrix: list[list[int]]) -> list[int]:
    """Read a matrix in clockwise spiral order.

    Approach: shrink top/bottom/left/right bounds after each side walk.
    Time: O(m * n)
    Space: O(1) besides the output
    Alternative: direction vector + visited set.
    Common bugs: reprinting the middle row/column without the top/bottom guards.
    """
    if not matrix:
        return []
    out = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out
