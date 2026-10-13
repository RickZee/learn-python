def greet(name: str = "world") -> str:
    return f"hello {name}"


def total(*args: int) -> int:
    result = 0
    for value in args:
        result = result + value
    return result


def append_copy(items: list[int], item: int) -> list[int]:
    copied = list(items)
    copied.append(item)
    return copied


def repeat(text: str, times: int = 1) -> str:
    return text * times
