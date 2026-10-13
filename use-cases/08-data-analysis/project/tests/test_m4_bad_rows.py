from pathlib import Path

from expenses.summary import parse_rows


def test_bad_amount_reports_line(tmp_path: Path):
    path = tmp_path / "bank.csv"
    path.write_text(
        "date,amount,memo\n2024-01-02,nope,coffee\n2024-01-03,5,rent\n", encoding="utf-8"
    )
    rows, errors = parse_rows(path)
    assert len(rows) == 1
    assert any("line 2" in message for message in errors)


def test_good_rows_still_returned(tmp_path: Path):
    path = tmp_path / "bank.csv"
    path.write_text(
        "date,amount,memo\n2024-01-02,nope,coffee\n2024-01-03,5,rent\n", encoding="utf-8"
    )
    rows, errors = parse_rows(path)
    assert len(errors) == 1
    assert rows[0].memo == "rent"
