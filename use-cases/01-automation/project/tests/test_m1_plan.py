from pathlib import Path

from tidy.sort import plan


def test_plan_groups_by_suffix(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    (tmp_path / "data.csv").write_text("b", encoding="utf-8")
    assert plan(tmp_path) == [("data.csv", "csv"), ("notes.txt", "txt")]


def test_plan_skips_undo_json(tmp_path: Path):
    (tmp_path / "undo.json").write_text("[]", encoding="utf-8")
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    assert plan(tmp_path) == [("a.txt", "txt")]
