from decimal import Decimal
from pathlib import Path

from expenses.summary import chart, over_budget


def test_over_budget(tmp_path: Path):
    budget = tmp_path / "budget.json"
    budget.write_text('{"food": "8"}', encoding="utf-8")
    totals = {"2024-01": {"food": Decimal("10"), "home": Decimal("20")}}
    assert over_budget(totals, budget) == [("2024-01", "food", Decimal("10"), Decimal("8"))]


def test_chart_writes_png(tmp_path: Path):
    csv_path = tmp_path / "bank.csv"
    csv_path.write_text("date,amount,memo\n2024-01-02,10,coffee\n", encoding="utf-8")
    rules = tmp_path / "rules.json"
    rules.write_text('{"coffee": "food"}', encoding="utf-8")
    image = tmp_path / "chart.png"
    chart(csv_path, image, rules)
    assert image.stat().st_size > 0
