def least_interval(tasks: list[str], n: int) -> int:
    """Minimum intervals to run all tasks with cool-down n between identical ones.

    Approach: formula from the most frequent task's skeleton, vs len(tasks).
    Time: O(T) for T tasks
    Space: O(1) for a fixed alphabet counter
    Alternative: simulate with a max-heap of remaining counts.
    Common bugs: forgetting peak_count; omitting max with len(tasks).
    """
    from collections import Counter

    counts = list(Counter(tasks).values())
    peak = max(counts)
    peak_count = counts.count(peak)
    return max(len(tasks), (peak - 1) * (n + 1) + peak_count)
