def parse_int(text: str):
    try:
        return int(text)
    except ValueError:
        return None


def safe_div(left: float, right: float) -> float | None:
    try:
        return left / right
    except ZeroDivisionError:
        return None


def safe_int(text: str):
    try:
        return int(text)
    except ValueError:
        return None
