def subset_count(nums: list[int]) -> int:
    return 2 ** len(nums)


def subsets(nums: list[int]) -> list[list[int]]:
    """Every subset. Order does not matter.

    Approach: for each value, recurse without it and with it, then undo.
    Time: O(n * 2^n)
    Space: O(n) for the current choice
    Alternative: bit masks from 0 to 2^n - 1.
    Common bugs: recording the choice list without copying it.
    """
    answers: list[list[int]] = []
    choice: list[int] = []

    def walk(index: int) -> None:
        if index == len(nums):
            answers.append(choice.copy())
            return
        walk(index + 1)
        choice.append(nums[index])
        walk(index + 1)
        choice.pop()

    walk(0)
    return answers


def listed(nums: list[int]) -> list[tuple[int, ...]]:
    return sorted(tuple(row) for row in subsets(nums))


def letter_case(text: str) -> list[str]:
    """Every way to change the case of the letters. Digits stay put.

    Approach: at each letter, recurse lower and upper.
    Time: O(2^k * n) where k is the number of letters
    Space: O(n) for the current string
    Alternative: the same walk building a list of characters.
    Common bugs: flipping digits.
    """
    answers: list[str] = []
    chars = list(text)

    def walk(index: int) -> None:
        if index == len(chars):
            answers.append("".join(chars))
            return
        walk(index + 1)
        if chars[index].isalpha():
            chars[index] = chars[index].swapcase()
            walk(index + 1)
            chars[index] = chars[index].swapcase()

    walk(0)
    return answers
