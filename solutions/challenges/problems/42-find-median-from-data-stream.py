
class MedianFinder:
    """Median of a stream.

    Approach: a max-heap for the low half and a min-heap for the high half.
    Time: O(log n) to add, O(1) to read
    Space: O(n)
    Alternative: keep a sorted list and insert with bisect.
    Common bugs: letting one heap grow more than one element ahead of the other.
    """

    def __init__(self) -> None:
        self.low: list[int] = []
        self.high: list[int] = []

    def add_num(self, num: int) -> None:
        import heapq

        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
