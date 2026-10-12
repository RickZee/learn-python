
def next_greater(nums: list[int]) -> list[int]:
    """Next strictly greater value to the right, or -1.

    Approach: a stack of indexes waiting for a greater value.
    Time: O(n)
    Space: O(n)
    Alternative: scan to the right for each index.
    Common bugs: using <= so equals count as greater.
    """
    answer = [-1] * len(nums)
    stack: list[int] = []
    for index, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            answer[stack.pop()] = value
        stack.append(index)
    return answer


class MinStack:
    """push, pop, top, and get_min. get_min is O(1).

    Approach: a second stack stores the minimum at each height.
    Time: O(1) for each call
    Space: O(n)
    Alternative: scan the stack for the minimum on each get_min.
    Common bugs: forgetting to pop the mins stack.
    """

    def __init__(self) -> None:
        self.values: list[int] = []
        self.mins: list[int] = []

    def push(self, value: int) -> None:
        self.values.append(value)
        smallest = value if not self.mins else min(value, self.mins[-1])
        self.mins.append(smallest)

    def pop(self) -> None:
        self.values.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.values[-1]

    def get_min(self) -> int:
        return self.mins[-1]


def minimum_after() -> int:
    stack = MinStack()
    stack.push(3)
    stack.push(1)
    stack.pop()
    return stack.get_min()
