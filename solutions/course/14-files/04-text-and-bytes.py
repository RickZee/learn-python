def as_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def as_text(data: bytes) -> str:
    return data.decode("utf-8")


def wire_size(text: str) -> int:
    data = text.encode("utf-8")
    size = len(data)
    result = int(size)
    return result


def decode_cafe() -> str:
    data = "café".encode("utf-8")
    return data.decode("utf-8")
