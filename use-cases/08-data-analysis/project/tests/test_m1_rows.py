from decimal import Decimal
from pathlib import Path

from expenses.summary import Row, parse_rows

SAMPLE = "date,amount,memo\n2024-01-02,10,coffee\n"


def test_parse_rows_uses_decimal(tmp_path: Path):
    path = tmp_path / "bank.csv"
    path.write_text(SAMPLE, encoding="utf-8")
    rows, errors = parse_rows(path)
    assert errors == []
    assert rows == [Row(date="2024-01-02", amount=Decimal("10"), memo="coffee")]


def test_parse_rows_type(tmp_path: Path):
    path = tmp_path / "bank.csv"
    path.write_text(SAMPLE, encoding="utf-8")
    rows, _ = parse_rows(path)
    assert isinstance(rows[0].amount, Decimal)
