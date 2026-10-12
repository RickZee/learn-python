def cleaned(raw: str) -> str:
    return raw.strip().lower()


def reversed_words(s: str) -> str:
    return " ".join(reversed(s.split()))


def normalize(raw: str) -> str:
    return " ".join(raw.split()).lower()
