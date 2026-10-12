import threading

from limiter.window import Window


class Limiter:
    def __init__(self, limit: int) -> None:
        self.window = Window(limit)
        self.total = 0
        self._lock = threading.Lock()

    def allow(self, key: str) -> bool:
        with self._lock:
            self.total += 1
            return self.window.hit(key)

    def reset(self, key: str) -> None:
        with self._lock:
            self.window.reset(key)
