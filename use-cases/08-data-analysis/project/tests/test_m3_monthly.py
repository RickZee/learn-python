from decimal import Decimal
from pathlib import Path

from expenses.summary import Row, monthly_totals


def test_monthly_totals_groups(tmp_path: Path):
    categorized = [
        (Row("2024-01-02", Decimal("10"), "coffee"), "food"),
        (Row("2024-01-15", Decimal("20"), "rent"), "home"),
        (Row("2024-02-01", Decimal("5"), "coffee"), "food"),
    ]
    assert monthly_totals(categorized) == {
        "2024-01": {"food": Decimal("10"), "home": Decimal("20")},
        "2024-02": {"food": Decimal("5")},
    }


def test_monthly_totals_sums_same_category():
    categorized = [
        (Row("2024-01-02", Decimal("10"), "a"), "food"),
        (Row("2024-01-03", Decimal("4"), "b"), "food"),
    ]
    assert monthly_totals(categorized)["2024-01"]["food"] == Decimal("14")
