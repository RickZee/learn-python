def length_of_lis(nums: list[int]) -> int:
    """Length of the longest strictly increasing subsequence.

    Approach: tails array with bisect_left (patience sorting).
    Time: O(n log n)
    Space: O(n)
    Alternative: O(n²) DP best[i] from earlier smaller values.
    Common bugs: bisect_right for strict LIS; treating tails as one subsequence.
    """
    import bisect

    tails = []
    for value in nums:
        i = bisect.bisect_left(tails, value)
        if i == len(tails):
            tails.append(value)
        else:
            tails[i] = value
    return len(tails)
