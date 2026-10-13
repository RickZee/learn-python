def countdown(n: int) -> list[int]:
    if n == 0:
        return []
    return [n] + countdown(n - 1)


def triangular(n: int) -> int:
    if n == 0:
        return 0
    rest = triangular(n - 1)
    total = n + rest
    return total


def product(nums: list[int]) -> int:
    if nums == []:
        return 1
    return nums[0] * product(nums[1:])


def digit_count(n: int) -> int:
    if n < 10:
        return 1
    return 1 + digit_count(n // 10)
