def add(a: int, b: int) -> int:
    return a + b


def bounds(nums: list[int]) -> tuple[int, int]:
    low = min(nums)
    high = max(nums)
    pair = (low, high)
    return pair


def plus_one(n: int) -> int:
    result = n + 1
    return result


def spread(nums: list[int]) -> int:
    return max(nums) - min(nums)
