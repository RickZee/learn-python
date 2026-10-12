def as_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def as_text(data: bytes) -> str:
    return data.decode("utf-8")


def wire_size(text: str) -> int:
    return len(text.encode("utf-8"))
