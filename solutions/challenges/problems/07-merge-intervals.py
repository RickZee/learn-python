def merge(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals, including ones that only touch.

    Approach: sort a copy by the start, then extend the last interval or append.
    Time: O(n log n)
    Space: O(n) for the copy and the answer
    Alternative: a sweep of start and end events.
    Common bugs: sorting by the end, or treating a touch at one point as a gap.
    """
    ordered = sorted(intervals, key=lambda span: span[0])
    if not ordered:
        return []
    merged = [ordered[0][:]]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
