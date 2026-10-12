import bisect


def insert_point(sorted_nums: list[int], value: int) -> int:
    return bisect.bisect_left(sorted_nums, value)


def keep_sorted(sorted_nums: list[int], value: int) -> list[int]:
    ordered = list(sorted_nums)
    bisect.insort(ordered, value)
    return ordered


def count_below(sorted_nums: list[int], limit: int) -> int:
    return bisect.bisect_left(sorted_nums, limit)
