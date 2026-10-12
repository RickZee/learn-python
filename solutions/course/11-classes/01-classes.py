class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def moved(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)

    def copy(self) -> "Point":
        return Point(self.x, self.y)
