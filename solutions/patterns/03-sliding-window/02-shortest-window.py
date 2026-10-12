def min_subarray_len(target: int, nums: list[int]) -> int:
    """Shortest subarray with sum at least target, or 0.

    Approach: grow the window, then shrink it while the sum still qualifies.
    Time: O(n)
    Space: O(1)
    Alternative: a prefix-sum binary search when values can be negative.
    Common bugs: shrinking past an empty window.
    """
    best = len(nums) + 1
    total = 0
    left = 0
    for right, value in enumerate(nums):
        total += value
        while total >= target and left <= right:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best > len(nums) else best


def all_unique(s: str) -> bool:
    seen = set()
    for character in s:
        if character in seen:
            return False
        seen.add(character)
    return True


def longest_letters(s: str) -> int:
    best = 0
    current = 0
    for character in s:
        if character.isalpha():
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best
