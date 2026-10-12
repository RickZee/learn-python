
def trap(height: list[int]) -> int:
    """Water trapped between bars.

    Approach: two pointers. The shorter side's max limits the water.
    Time: O(n)
    Space: O(1)
    Alternative: a prefix max and a suffix max.
    Common bugs: adding water on the pointer you have not updated the max for.
    """
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
