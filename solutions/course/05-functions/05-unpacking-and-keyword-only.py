def tag(n: int, /, *, label: str = "n") -> str:
    return label + ":" + str(n)


def combine(x: int, y: int, *, scale: int = 1) -> int:
    return (x + y) * scale


def scaled_pair(values: list[int], options: dict[str, int]) -> int:
    return combine(*values, **options)
