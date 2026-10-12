import time

from limiter.window import Window


class Limiter:
    def __init__(self, limit: int) -> None:
        self.window = Window(limit)
        self.total = 0

    def allow(self, key: str) -> bool:
        # Planted race: read-modify-write without a lock.
        current = self.total
        time.sleep(0.0001)
        self.total = current + 1
        return self.window.hit(key)

    def reset(self, key: str) -> None:
        self.window.reset(key)
