from decimal import Decimal
from pathlib import Path

from watch.prices import parse_price

HTML = Path(__file__).parents[1].joinpath("fixtures", "item.html").read_text(encoding="utf-8")


def test_parse_price_from_fixture():
    assert parse_price(HTML) == Decimal("12.50")


def test_parse_price_type():
    assert isinstance(parse_price(HTML), Decimal)
