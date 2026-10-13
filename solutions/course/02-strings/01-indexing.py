def last(s: str) -> str:
    return s[-1]


def ends(s: str) -> str:
    if s == "":
        return ""
    first = s[0]
    last_char = s[-1]
    return first + last_char


def tail_two(s: str) -> str:
    return s[-2:]


def is_palindrome(s: str) -> bool:
    return s == s[::-1]
