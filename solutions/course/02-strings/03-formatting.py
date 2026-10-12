def items(n: int) -> str:
    return f"{n} items"


def describe_score(name: str, score: int) -> str:
    return f"{name} has {score}"


def describe_exact(name: str, score: int) -> str:
    return f"{name!r} has {score}"
