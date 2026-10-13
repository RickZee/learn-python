from pathlib import Path


def plan(folder: Path) -> list[tuple[str, str]]:
    """Return (filename, destination folder name) pairs. Do not move files."""
    raise NotImplementedError


def apply(folder: Path, dry_run: bool = False) -> list[tuple[str, str]]:
    """Move files unless dry_run. Write undo.json when you really move them."""
    raise NotImplementedError


def undo(folder: Path) -> list[tuple[str, str]]:
    """Restore files listed in undo.json to the folder root."""
    raise NotImplementedError


def summary(folder: Path) -> dict[str, int]:
    """Count planned files per suffix folder name."""
    raise NotImplementedError
