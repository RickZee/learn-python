from collections import deque


def window_max(nums: list[int], k: int) -> list[int]:
    out = []
    dq = deque()
    for i, value in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= value:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
