def rotate_image(matrix: list[list[int]]) -> list[list[int]]:
    """Rotate an n×n matrix 90° clockwise in place.

    Approach: transpose across the diagonal, then reverse each row.
    Time: O(n²)
    Space: O(1)
    Alternative: four-way swaps on concentric rings; copy into a new matrix.
    Common bugs: double-swapping off-diagonal by looping j from 0; reversing columns.
    """
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix
