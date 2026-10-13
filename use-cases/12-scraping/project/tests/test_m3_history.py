from decimal import Decimal
from pathlib import Path

from watch.prices import last_price, record_price


def test_record_and_read(tmp_path: Path):
    database = tmp_path / "prices.db"
    record_price(database, "item-1", Decimal("10.00"))
    assert last_price(database, "item-1") == Decimal("10.00")


def test_last_price_is_newest(tmp_path: Path):
    database = tmp_path / "prices.db"
    record_price(database, "item-1", Decimal("10.00"))
    record_price(database, "item-1", Decimal("9.00"))
    assert last_price(database, "item-1") == Decimal("9.00")
