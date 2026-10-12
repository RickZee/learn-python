class Window:
    def __init__(self, limit: int, counts: dict[str, int] | None = None) -> None:
        self.limit = limit
        self.counts = {} if counts is None else counts

    def hit(self, key: str) -> bool:
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key] <= self.limit

    def reset(self, key: str) -> None:
        self.counts[key] = 0
