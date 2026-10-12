def single_number_bit(nums: list[int]) -> int:
    acc = 0
    for value in nums:
        acc = acc ^ value
    return acc
