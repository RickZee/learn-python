def exist(board: list[list[str]], word: str) -> bool:
    """True when word is a path of adjacent cells, each used once.

    Approach: backtracking. Mark the cell, try four neighbors, then restore it.
    Time: O(rows * cols * 4^len(word))
    Space: O(len(word)) for the call stack
    Alternative: the same walk with an explicit stack.
    Common bugs: forgetting to restore the letter, so later paths see a hole.
    """
    rows, cols = len(board), len(board[0])

    def walk(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True
        if not (0 <= row < rows and 0 <= col < cols) or board[row][col] != word[index]:
            return False
        letter = board[row][col]
        board[row][col] = "#"
        found = any(
            walk(row + drow, col + dcol, index + 1)
            for drow, dcol in ((1, 0), (-1, 0), (0, 1), (0, -1))
        )
        board[row][col] = letter
        return found

    return any(walk(row, col, 0) for row in range(rows) for col in range(cols))
