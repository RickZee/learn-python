from pathlib import Path

from watch.prices import parse_price, remember

HTML = Path(__file__).parents[1].joinpath("fixtures", "item.html").read_text(encoding="utf-8")


def test_parse_price_from_the_fixture():
    assert parse_price(HTML) == "12.50"


def test_remember_uses_the_stored_price(tmp_path: Path):
    database = tmp_path / "prices.db"
    assert remember(database, HTML) == "12.50"
    assert remember(database, "<html></html>") == "12.50"
