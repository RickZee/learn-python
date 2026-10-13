import re


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text)


def numbers(text: str) -> list[str]:
    pattern = r"\d+"
    matches = re.findall(pattern, text)
    result = list(matches)
    return result


def quoted(text: str) -> list[str]:
    pattern = r'"([^"]*)"'
    matches = re.findall(pattern, text)
    return matches


def redact(text: str) -> str:
    return re.sub(r"\bspam\b", "****", text)
