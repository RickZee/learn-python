

def overlaps(left: list[int], right: list[int]) -> bool:
    return left[0] <= right[1] and right[0] <= left[1]



def can_attend(intervals: list[list[int]]) -> bool:
    """True when no two meetings overlap. Touching at an endpoint is allowed.

    Approach: sort by the start and compare each start with the previous end.
    Time: O(n log n)
    Space: O(n) for the sorted copy
    Alternative: a sweep of start and end events.
    Common bugs: treating a shared endpoint as an overlap.
    """
    ordered = sorted(intervals)
    return all(ordered[index][0] >= ordered[index - 1][1] for index in range(1, len(ordered)))

def covered(intervals: list[list[int]]) -> int:
    return sum(end - start for start, end in intervals)
