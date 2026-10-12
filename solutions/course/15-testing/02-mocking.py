import os
from pathlib import Path


def mode_label() -> str:
    return os.environ.get("APP_MODE", "live")


def run_label() -> str:
    if os.environ.get("APP_MODE", "live") == "test":
        return "dry-run"
    return "live"


def read_title(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    if not text:
        return ""
    return text.splitlines()[0]
