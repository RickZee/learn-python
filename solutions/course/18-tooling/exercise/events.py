import logging

log = logging.getLogger("tooling")


def log_event(message: str) -> None:
    log.info(message)
