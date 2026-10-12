import json

from pylearn import load_exercise


def test_summarize_writes_rows_and_qty(tmp_path):
    source = tmp_path / "items.csv"
    source.write_text("name,qty\nada,2\nbea,3\n", encoding="utf-8")
    target = tmp_path / "summary.json"
    load_exercise("summary").summarize(str(source), str(target))
    assert json.loads(target.read_text(encoding="utf-8")) == {"rows": 2, "qty": 5}


def test_empty_csv_is_zero(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text("name,qty\n", encoding="utf-8")
    target = tmp_path / "summary.json"
    load_exercise("summary").summarize(str(source), str(target))
    assert json.loads(target.read_text(encoding="utf-8")) == {"rows": 0, "qty": 0}
