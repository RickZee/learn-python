def subarray_sum(nums: list[int], k: int) -> int:
    """Count contiguous subarrays that sum to k.

    Approach: prefix sums in a hash map. At total T, add counts[T - k].
    Time: O(n)
    Space: O(n)
    Alternative: O(n²) expand every left endpoint.
    Common bugs: forgetting counts[0] = 1; sliding window with negatives.
    """
    from collections import defaultdict

    counts = defaultdict(int)
    counts[0] = 1
    total = answer = 0
    for value in nums:
        total += value
        answer += counts[total - k]
        counts[total] += 1
    return answer
