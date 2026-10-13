def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Combinations that sum to target. A candidate may be reused.

    Approach: backtracking in sorted order, reusing by staying at the same index.
    Time: exponential in the target
    Space: O(target) for the current combination
    Alternative: dynamic programming of the combinations for each remainder.
    Common bugs: moving the index when you meant to reuse the same candidate.
    """
    ordered = sorted(candidates)
    answers: list[list[int]] = []
    choice: list[int] = []

    def walk(start: int, remain: int) -> None:
        if remain == 0:
            answers.append(choice.copy())
            return
        for index in range(start, len(ordered)):
            if ordered[index] > remain:
                break
            choice.append(ordered[index])
            walk(index, remain - ordered[index])
            choice.pop()

    walk(0, target)
    return answers
