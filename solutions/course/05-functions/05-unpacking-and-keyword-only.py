def tag(n: int, /, *, label: str = "n") -> str:
    return label + ":" + str(n)


def combine(x: int, y: int, *, scale: int = 1) -> int:
    total = x + y
    factor = scale
    scaled = total * factor
    return scaled


def tagged(n: int, *, label: str = "n") -> str:
    return label + ":" + str(n)


def scaled_pair(values: list[int], options: dict[str, int]) -> int:
    return combine(*values, **options)
