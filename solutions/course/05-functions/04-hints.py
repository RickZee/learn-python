def hello(name: str) -> str:
    """Return a greeting for name."""
    return "hello " + name


def labeled(n: int) -> str:
    """Return the number as text."""
    text = str(n)
    result = text
    as_text = str(result)
    return as_text


def add_numbers(a: int, b: int) -> int:
    return a + b


def hint_keys() -> list[str]:
    return sorted(labeled.__annotations__)
