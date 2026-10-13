import bisect


def insert_point(sorted_nums: list[int], value: int) -> int:
    return bisect.bisect_left(sorted_nums, value)


def keep_sorted(nums: list[int], value: int) -> list[int]:
    ordered = sorted(nums)
    bisect.insort(ordered, value)
    result = list(ordered)
    return result


def count_below(sorted_nums: list[int], limit: int) -> int:
    return bisect.bisect_left(sorted_nums, limit)
