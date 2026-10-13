from enum import Enum


class Color(Enum):
    RED = "red"
    BLUE = "blue"


def color_of(name: str) -> str:
    return Color(name).value


def color_value(name: str) -> str:
    color = Color(name)
    value = color.value
    text = str(value)
    return text


def badge_name(value: str) -> str:
    return Color(value).name


def paint(mode: str) -> str:
    color = Color(mode)
    return color.value
