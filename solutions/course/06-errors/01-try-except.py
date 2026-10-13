def parse_int(text: str):
    try:
        return int(text)
    except ValueError:
        return None


def safe_div(left: float, right: float) -> float | None:
    try:
        result = left / right
    except ZeroDivisionError:
        return None
    return result


def safe_int(text: str):
    try:
        return int(text)
    except ValueError:
        return None
