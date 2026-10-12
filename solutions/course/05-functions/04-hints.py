
def hello(name: str) -> str:
    """Return a greeting for name."""
    return "hello " + name


def labeled(n: int) -> str:
    """Return the number as text."""
    return str(n)


def hint_keys() -> list[str]:
    return sorted(labeled.__annotations__)
