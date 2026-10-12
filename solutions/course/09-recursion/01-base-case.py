def countdown(n: int) -> list[int]:
    if n == 0:
        return []
    return [n] + countdown(n - 1)


def triangular(n: int) -> int:
    if n == 0:
        return 0
    return n + triangular(n - 1)


def product(nums: list[int]) -> int:
    if nums == []:
        return 1
    return nums[0] * product(nums[1:])
