from decimal import Decimal
from pathlib import Path

from expenses.summary import Row, categorize


def test_categorize_known_memo(tmp_path: Path):
    rules = tmp_path / "rules.json"
    rules.write_text('{"coffee": "food"}', encoding="utf-8")
    rows = [Row("2024-01-02", Decimal("10"), "coffee")]
    assert categorize(rows, rules) == [(rows[0], "food")]


def test_categorize_unknown_is_other(tmp_path: Path):
    rules = tmp_path / "rules.json"
    rules.write_text("{}", encoding="utf-8")
    rows = [Row("2024-01-02", Decimal("10"), "taxi")]
    assert categorize(rows, rules) == [(rows[0], "other")]
