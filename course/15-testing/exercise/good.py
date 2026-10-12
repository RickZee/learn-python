def word_count(text: str) -> int:
    return len(text.split())


def shout(text: str) -> str:
    return text.upper()


def first_word(text: str) -> str:
    words = text.split()
    if not words:
        return ""
    return words[0]
