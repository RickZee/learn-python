import json
from pathlib import Path


def plan(folder: Path) -> list[tuple[str, str]]:
    moves = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.name != "undo.json" and path.suffix:
            moves.append((path.name, path.suffix.lstrip(".")))
    return moves


def apply(folder: Path, dry_run: bool = False) -> list[tuple[str, str]]:
    moves = plan(folder)
    if dry_run:
        return moves
    for name, kind in moves:
        target = folder / kind
        target.mkdir(exist_ok=True)
        (folder / name).rename(target / name)
    (folder / "undo.json").write_text(json.dumps(moves), encoding="utf-8")
    return moves
