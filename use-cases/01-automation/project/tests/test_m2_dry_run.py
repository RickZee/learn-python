from pathlib import Path

from tidy.sort import apply


def test_dry_run_does_not_move(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    moves = apply(tmp_path, dry_run=True)
    assert moves == [("notes.txt", "txt")]
    assert (tmp_path / "notes.txt").exists()
    assert not (tmp_path / "undo.json").exists()


def test_dry_run_returns_full_plan(tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.csv").write_text("b", encoding="utf-8")
    assert apply(tmp_path, dry_run=True) == [("a.txt", "txt"), ("b.csv", "csv")]
