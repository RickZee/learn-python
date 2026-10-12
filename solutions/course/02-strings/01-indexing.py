def last(s: str) -> str:
    return s[-1]


def is_palindrome(s: str) -> bool:
    return s == s[::-1]


def ends(s: str) -> str:
    if s == "":
        return ""
    return s[0] + s[-1]
