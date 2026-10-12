def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Minimum rooms so no two overlapping meetings share a room.

    Approach: sort by start; min-heap of end times; reuse when earliest end ≤ start.
    Time: O(n log n)
    Space: O(n)
    Alternative: sweep line on sorted starts and ends.
    Common bugs: sorting by end; using < instead of <= for touching intervals.
    """
    import heapq

    if not intervals:
        return 0
    intervals = sorted(intervals)
    rooms = []
    for start, end in intervals:
        if rooms and rooms[0] <= start:
            heapq.heappop(rooms)
        heapq.heappush(rooms, end)
    return len(rooms)
