def single_number(nums: list[int]) -> int:
    """Find the value that appears once when every other appears twice.

    Approach: XOR all values; pairs cancel, the singleton remains.
    Time: O(n)
    Space: O(1)
    Alternative: hash set add/remove; sort and scan.
    Common bugs: using + or | instead of ^; hashing when O(1) space is required.
    """
    acc = 0
    for value in nums:
        acc ^= value
    return acc
