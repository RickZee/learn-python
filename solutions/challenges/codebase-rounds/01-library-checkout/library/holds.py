from collections import deque


class HoldQueue:
    def __init__(self) -> None:
        self.waiting: deque[str] = deque()

    def join(self, patron: str) -> None:
        self.waiting.append(patron)

    def next(self) -> str:
        return self.waiting.popleft()
