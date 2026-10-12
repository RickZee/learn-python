def product_except_self(nums: list[int]) -> list[int]:
    """answer[i] is the product of every element except nums[i]. No division.

    Approach: a left-to-right pass, then a right-to-left pass.
    Time: O(n)
    Space: O(1) extra, aside from the answer
    Alternative: divide the total product by each value, and handle zeros apart.
    Common bugs: writing the running product into the answer before the current value is excluded.
    """
    answer = [1] * len(nums)
    prefix = 1
    for index, value in enumerate(nums):
        answer[index] = prefix
        prefix *= value
    suffix = 1
    for index in range(len(nums) - 1, -1, -1):
        answer[index] *= suffix
        suffix *= nums[index]
    return answer
