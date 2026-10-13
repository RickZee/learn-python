def require_name(name: str) -> str:
    if name == "":
        raise ValueError("empty")
    return name


def parse_age(text: str) -> int:
    try:
        n = int(text)
    except ValueError as err:
        raise ValueError("not an int") from err
    if n < 0:
        raise ValueError("negative")
    return n


def parse_name(text: str) -> str:
    if text == "":
        raise ValueError("empty")
    return text
