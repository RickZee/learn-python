from pathlib import Path

from tidy.sort import plan, summary


def test_plan_skips_hidden(tmp_path: Path):
    (tmp_path / ".secret.txt").write_text("x", encoding="utf-8")
    (tmp_path / "visible.txt").write_text("y", encoding="utf-8")
    assert plan(tmp_path) == [("visible.txt", "txt")]


def test_summary_counts(tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "c.csv").write_text("c", encoding="utf-8")
    assert summary(tmp_path) == {"txt": 2, "csv": 1}
