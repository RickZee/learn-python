import math


def hypotenuse(a: float, b: float) -> float:
    return math.hypot(a, b)


def square_root(n: float) -> float:
    return math.sqrt(n)


def circumference(radius: float) -> float:
    diameter = radius * 2
    length = math.pi * diameter
    result = float(length)
    return result


def module_identity() -> bool:
    import sys
    import math

    first = id(sys.modules["math"])
    import math

    second = id(sys.modules["math"])
    return first == second
