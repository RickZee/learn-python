from pathlib import Path

from tidy.sort import apply


def test_apply_moves_and_writes_undo(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("a", encoding="utf-8")
    apply(tmp_path, dry_run=False)
    assert (tmp_path / "txt" / "notes.txt").read_text(encoding="utf-8") == "a"
    assert "notes.txt" in (tmp_path / "undo.json").read_text(encoding="utf-8")


def test_collision_renames(tmp_path: Path):
    dest = tmp_path / "txt"
    dest.mkdir()
    (dest / "notes.txt").write_text("old", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("new", encoding="utf-8")
    apply(tmp_path, dry_run=False)
    assert (dest / "notes.txt").read_text(encoding="utf-8") == "old"
    assert (dest / "notes (1).txt").read_text(encoding="utf-8") == "new"
