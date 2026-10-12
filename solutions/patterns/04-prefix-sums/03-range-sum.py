

def product_all(nums: list[int]) -> int:
    result = 1
    for value in nums:
        result *= value
    return result


def zero_count(nums: list[int]) -> int:
    return sum(value == 0 for value in nums)

def range_sum(nums: list[int], left: int, right: int) -> int:
    """Return the sum of nums[left] through nums[right], inclusive.

    Approach: one prefix array, then two lookups.
    Time: O(n) to build, O(1) per query if you kept the prefix
    Space: O(n)
    Alternative: sum of the slice.
    Common bugs: an off-by-one on the right index.
    """
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return prefix[right + 1] - prefix[left]
