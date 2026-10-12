def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """Maximum value in every contiguous window of size k.

    Approach: monotonic deque of indexes, front is the window max.
    Time: O(n)
    Space: O(k)
    Alternative: scan each window in O(k), or a heap with lazy expiry.
    Common bugs: storing values instead of indexes; emitting before i >= k - 1.
    """
    from collections import deque

    dq, out = deque(), []
    for i, value in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= value:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
