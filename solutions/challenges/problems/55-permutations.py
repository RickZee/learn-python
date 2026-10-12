def permute(nums: list[int]) -> list[list[int]]:
    """All permutations of a list of distinct numbers.

    Approach: swap-based backtracking fixing each start index in turn.
    Time: O(n * n!)
    Space: O(n) besides the output
    Alternative: used[] flags with an explicit path; itertools.permutations.
    Common bugs: appending the live list without copying; not swapping back.
    """
    nums = list(nums)
    out = []

    def go(start):
        if start == len(nums):
            out.append(list(nums))
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            go(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    go(0)
    return out
