def sign(n: int) -> str:
    if n > 0:
        return "positive"
    if n == 0:
        return "zero"
    return "negative"


def grade(score: int | None) -> str:
    if score is None:
        return "missing"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    return "C"


def first_present(a, b, c):
    if a is not None:
        return a
    if b is not None:
        return b
    return c
