class NegativeAgeError(Exception):
    pass


def require_age(age: int) -> int:
    if age < 0:
        raise NegativeAgeError("negative")
    return age


def parse_age(age: int) -> int:
    return require_age(age)


def form_error() -> str:
    try:
        raise NegativeAgeError("negative")
    except NegativeAgeError as error:
        return str(error)
