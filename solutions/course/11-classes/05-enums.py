
from enum import Enum


class Color(Enum):
    RED = "red"
    BLUE = "blue"


def color_of(name: str) -> str:
    return Color(name).value


def color_value(name: str) -> str:
    return Color(name).value


def badge_name(value: str) -> str:
    return Color(value).name
