
def require_name(name: str) -> str:
    if name == "":
        raise ValueError("empty")
    return name


def parse_age(text: str) -> int:
    n = int(text)
    if n < 0:
        raise ValueError("negative")
    return n


def parse_name(text: str) -> str:
    if text == "":
        raise ValueError("empty")
    return text
