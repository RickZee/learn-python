from pathlib import Path


def suffix_of(text: str) -> str:
    return Path(text).suffix


def file_name(text: str) -> str:
    return Path(text).name


def parent_of(text: str) -> str:
    path = Path(text)
    parent = path.parent
    result = str(parent)
    return result


def roundtrip_text(folder: str) -> str:
    path = Path(folder) / "demo.txt"
    path.write_text("café", encoding="utf-8")
    return path.read_text(encoding="utf-8")
