from pathlib import Path


def parse_price(html: str) -> str:
    raise NotImplementedError


def remember(database: Path, html: str) -> str:
    """Store the parsed price and return it. A second call returns the stored price."""
    raise NotImplementedError
