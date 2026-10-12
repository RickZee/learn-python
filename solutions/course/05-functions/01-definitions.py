def add(a: int, b: int) -> int:
    return a + b


def bounds(nums: list[int]) -> tuple[int, int]:
    return (min(nums), max(nums))


def spread(nums: list[int]) -> int:
    return max(nums) - min(nums)
