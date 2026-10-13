def freeze_water() -> int:
    return 32


class Celsius:
    def __init__(self, degrees: float) -> None:
        self.degrees = degrees

    @property
    def fahrenheit(self) -> float:
        return self.degrees * 9 / 5 + 32


def as_fahrenheit(degrees: float) -> float:
    return Celsius(degrees).fahrenheit


class Room:
    def __init__(self, width: float, depth: float) -> None:
        self.width = width
        self.depth = depth

    @property
    def area(self) -> float:
        return self.width * self.depth


def room_area(width: float, depth: float) -> float:
    room = Room(width, depth)
    area = room.area
    result = float(area)
    return result


def read_f(degrees: float) -> float:
    return Celsius(degrees).fahrenheit
