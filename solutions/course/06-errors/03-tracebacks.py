
def error_name() -> str:
    try:
        [0][1]
    except IndexError:
        return "IndexError"
    return ""


def division_name() -> str:
    try:
        return str(1 // 0)
    except ZeroDivisionError:
        return "ZeroDivisionError"


def error_text() -> str:
    try:
        raise ValueError("negative")
    except ValueError as error:
        return str(error)
