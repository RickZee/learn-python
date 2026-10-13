from pathlib import Path

from tidy.sort import apply, undo


def test_undo_restores(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    apply(tmp_path, dry_run=False)
    undo(tmp_path)
    assert (tmp_path / "notes.txt").read_text(encoding="utf-8") == "a"


def test_undo_returns_pairs(tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    apply(tmp_path, dry_run=False)
    assert undo(tmp_path) == [("a.txt", "txt")]
