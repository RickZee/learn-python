class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def moved(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)

    def copy(self) -> "Point":
        return Point(self.x, self.y)


class Bag:
    def __init__(self, name: str) -> None:
        self.name = name
        self.tags = []


def make_bags() -> list:
    first = Bag("a")
    second = Bag("b")
    first.tags.append("x")
    return [first.tags, second.tags]


def shift_point(x: int, y: int, dx: int, dy: int) -> tuple[int, int]:
    point = Point(x, y)
    moved = point.moved(dx, dy)
    result = (moved.x, moved.y)
    return result
