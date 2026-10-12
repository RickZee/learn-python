import io
import logging


def contains_ready(message: str) -> bool:
    return "ready" in message


def is_ready(message: str) -> bool:
    return message == "ready"


def info_ready() -> str:
    buffer = io.StringIO()
    log = logging.getLogger("stretch")
    log.handlers = [logging.StreamHandler(buffer)]
    log.setLevel(logging.INFO)
    log.propagate = False
    log.info("ready")
    return buffer.getvalue()
