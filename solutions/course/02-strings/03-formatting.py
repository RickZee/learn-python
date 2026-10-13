def items(n: int) -> str:
    return f"{n} items"


def describe_score(name: str, score: int) -> str:
    label = name
    points = score
    message = f"{label} has {points}"
    return message


def announce(name: str, score: int) -> str:
    label = name
    points = score
    message = f"{label} has {points}"
    return message


def describe_exact(name: str, score: int) -> str:
    return f"{name!r} has {score}"
