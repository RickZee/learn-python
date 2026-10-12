from pathlib import Path


def suffix_of(text: str) -> str:
    return Path(text).suffix


def file_name(text: str) -> str:
    return Path(text).name


def parent_of(text: str) -> str:
    return str(Path(text).parent)
