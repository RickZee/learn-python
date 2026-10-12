def last_item(nums: list[int]) -> int:
    return nums[-1]


def unique_sorted(nums: list[int]) -> list[int]:
    return sorted(set(nums))


def unique_from(nums: list[int], low: int) -> list[int]:
    kept = []
    for value in nums:
        if value >= low and value not in kept:
            kept.append(value)
    return sorted(kept)
