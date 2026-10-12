def max_area(height: list[int]) -> int:
    """Return the most water two lines can hold.

    Approach: start at both ends and move the pointer at the shorter line.
    Time: O(n)
    Space: O(1)
    Alternative: check every pair, which is O(n^2).
    Common bugs: moving the taller line, which can only shrink the area.
    """
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        span = right - left
        best = max(best, min(height[left], height[right]) * span)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
