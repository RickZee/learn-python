from __future__ import annotations

from decimal import Decimal
from pathlib import Path


def parse_price(html: str) -> Decimal | None:
    raise NotImplementedError


def record_price(database: Path, item_id: str, price: Decimal) -> None:
    raise NotImplementedError


def last_price(database: Path, item_id: str) -> Decimal | None:
    raise NotImplementedError


def should_alert(previous: Decimal, current: Decimal, percent: float) -> bool:
    raise NotImplementedError


def fetch_price(client, url: str) -> Decimal | None:
    raise NotImplementedError
