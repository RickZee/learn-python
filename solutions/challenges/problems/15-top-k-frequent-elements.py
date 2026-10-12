def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Return the k values that appear most often. Order does not matter.

    Approach: count with Counter, then take the k most common.
    Time: O(n)
    Space: O(n)
    Alternative: bucket the values by their count.
    Common bugs: sorting the values instead of the counts, or returning counts instead of values.
    """
    from collections import Counter

    counts = Counter(nums)
    return [value for value, _count in counts.most_common(k)]
