from decimal import Decimal
from pathlib import Path

from watch.prices import parse_price

FIX = Path(__file__).parents[1] / "fixtures"


def test_us_format():
    html = (FIX / "us_price.html").read_text(encoding="utf-8")
    assert parse_price(html) == Decimal("1299.00")


def test_eu_format_and_missing():
    html = (FIX / "eu_price.html").read_text(encoding="utf-8")
    assert parse_price(html) == Decimal("1299.00")
    missing = (FIX / "missing.html").read_text(encoding="utf-8")
    assert parse_price(missing) is None
