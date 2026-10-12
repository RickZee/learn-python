
def generate_parenthesis(n: int) -> list[str]:
    """Every valid string of n pairs.

    Approach: open while pairs remain, close while closes are behind opens.
    Time: proportional to the Catalan number
    Space: O(n) for the current string
    Alternative: insert a pair into every valid string of n-1 pairs, then unique them.
    Common bugs: allowing a close before a matching open.
    """
    answers: list[str] = []

    def walk(opened: int, closed: int, path: str) -> None:
        if len(path) == 2 * n:
            answers.append(path)
            return
        if opened < n:
            walk(opened + 1, closed, path + "(")
        if closed < opened:
            walk(opened, closed + 1, path + ")")

    walk(0, 0, "")
    return answers
