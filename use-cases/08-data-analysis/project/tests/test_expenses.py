from pathlib import Path

from expenses.summary import chart, monthly

SAMPLE = "date,amount,memo\n2024-01-02,10,coffee\n2024-01-15,20,rent\n2024-02-01,5,coffee\n"


def test_monthly_categories(tmp_path: Path):
    csv_path = tmp_path / "bank.csv"
    csv_path.write_text(SAMPLE, encoding="utf-8")
    assert monthly(csv_path) == {"2024-01": {"food": 10, "home": 20}, "2024-02": {"food": 5}}


def test_chart_writes_a_png(tmp_path: Path):
    csv_path = tmp_path / "bank.csv"
    csv_path.write_text(SAMPLE, encoding="utf-8")
    image = tmp_path / "chart.png"
    chart(csv_path, image)
    assert image.stat().st_size > 0
