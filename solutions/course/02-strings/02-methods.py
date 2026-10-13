def cleaned(raw: str) -> str:
    return raw.strip().lower()


def normalize(raw: str) -> str:
    trimmed = raw.strip()
    parts = trimmed.split()
    joined = " ".join(parts)
    return joined.lower()


def tidy(raw: str) -> str:
    cleaned = raw.strip()
    lowered = cleaned.lower()
    return lowered


def reversed_words(s: str) -> str:
    parts = s.split()
    return " ".join(reversed(parts))
