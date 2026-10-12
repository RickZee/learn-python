import re


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text)


def numbers(text: str) -> list[str]:
    return re.findall(r"\d+", text)


def redact(text: str) -> str:
    return re.sub(r"\bspam\b", "****", text)
