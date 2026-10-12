def greet(name: str = "world") -> str:
    return f"hello {name}"


def total(*args: int) -> int:
    return sum(args)


def repeat(text: str, times: int = 1) -> str:
    return text * times
