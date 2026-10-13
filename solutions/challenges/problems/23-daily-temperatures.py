def daily_temperatures(temperatures: list[int]) -> list[int]:
    """Days until a warmer temperature, or 0.

    Approach: a stack of indexes in decreasing temperature order.
    Time: O(n)
    Space: O(n)
    Alternative: scan forward from each day.
    Common bugs: storing temperatures instead of indexes, so the distance is lost.
    """
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for index, temperature in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temperature:
            earlier = stack.pop()
            answer[earlier] = index - earlier
        stack.append(index)
    return answer
