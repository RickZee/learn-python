class TimeMap:
    def __init__(self):
        self.data = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.data.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        import bisect

        items = self.data.get(key, [])
        i = bisect.bisect_right(items, (timestamp, chr(127))) - 1
        return items[i][1] if i >= 0 else ""
