import copy


def snapshot(nums: list[int]) -> list[int]:
    return nums[:]


def own_rows(grid: list[list[int]]) -> list[list[int]]:
    copied = []
    for row in grid:
        copied.append(row[:])
    return copied


def detach_first_row(grid: list[list[int]]) -> list[list[int]]:
    copied = []
    for row in grid:
        copied.append(row[:])
    return copied


def detached(grid: list[list[int]]) -> list[list[int]]:
    return copy.deepcopy(grid)
