def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """Insert new into sorted non-overlapping intervals and merge.

    Approach: copy the intervals that end first, merge the overlap, then copy the rest.
    Time: O(n)
    Space: O(n)
    Alternative: append and run the full merge-intervals sort.
    Common bugs: treating a shared endpoint as a gap.
    """
    result = []
    index = 0
    while index < len(intervals) and intervals[index][1] < new[0]:
        result.append(intervals[index])
        index += 1
    while index < len(intervals) and intervals[index][0] <= new[1]:
        new = [min(new[0], intervals[index][0]), max(new[1], intervals[index][1])]
        index += 1
    result.append(new)
    result.extend(intervals[index:])
    return result
