from pathlib import Path


def plan(folder: Path) -> list[tuple[str, str]]:
    """Return (filename, destination folder name) pairs. Do not move files."""
    raise NotImplementedError


def apply(folder: Path, dry_run: bool = False) -> list[tuple[str, str]]:
    """Move files unless dry_run. Write undo.json when you really move them."""
    raise NotImplementedError
