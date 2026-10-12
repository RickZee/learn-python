from pathlib import Path

from tidy.sort import apply, plan


def test_plan_groups_by_suffix(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    (tmp_path / "data.csv").write_text("b", encoding="utf-8")
    assert plan(tmp_path) == [("data.csv", "csv"), ("notes.txt", "txt")]


def test_dry_run_does_not_move(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    apply(tmp_path, dry_run=True)
    assert (tmp_path / "notes.txt").exists()
    assert not (tmp_path / "undo.json").exists()


def test_apply_moves_and_writes_undo(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    apply(tmp_path, dry_run=False)
    assert (tmp_path / "txt" / "notes.txt").read_text(encoding="utf-8") == "a"
    assert "notes.txt" in (tmp_path / "undo.json").read_text(encoding="utf-8")
