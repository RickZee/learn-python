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
        message = str(error)
        return message


def checked_age(age: int) -> int:
    try:
        if age < 0:
            raise NegativeAgeError("negative")
        return age
    except NegativeAgeError:
        return 0
