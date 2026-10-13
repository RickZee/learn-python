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


def temp_mode() -> str:
    previous = os.environ.get("APP_MODE")
    os.environ["APP_MODE"] = "test"
    value = os.environ["APP_MODE"]
    if previous is None:
        os.environ.pop("APP_MODE", None)
    else:
        os.environ["APP_MODE"] = previous
    return value
