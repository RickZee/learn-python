from concurrent.futures import ThreadPoolExecutor


def squares(nums: list[int]) -> list[int]:
    def square(value: int) -> int:
        return value * value

    with ThreadPoolExecutor(max_workers=2) as pool:
        return list(pool.map(square, nums))


def doubled(nums: list[int]) -> list[int]:
    def double(value: int) -> int:
        return value * 2

    with ThreadPoolExecutor(max_workers=2) as pool:
        return list(pool.map(double, nums))


def sum_squares(nums: list[int]) -> int:
    return sum(squares(nums))
