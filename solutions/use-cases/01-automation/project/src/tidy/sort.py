import json
from collections import Counter
from pathlib import Path


def plan(folder: Path) -> list[tuple[str, str]]:
    moves = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        if path.name == "undo.json" or path.name.startswith("."):
            continue
        if not path.suffix:
            continue
        moves.append((path.name, path.suffix.lstrip(".")))
    return moves


def _unique_target(folder: Path, name: str) -> str:
    candidate = folder / name
    if not candidate.exists():
        return name
    stem = Path(name).stem
    suffix = Path(name).suffix
    index = 1
    while True:
        alt = f"{stem} ({index}){suffix}"
        if not (folder / alt).exists():
            return alt
        index += 1


def apply(folder: Path, dry_run: bool = False) -> list[tuple[str, str]]:
    moves = plan(folder)
    if dry_run:
        return moves
    recorded: list[tuple[str, str, str]] = []
    for name, kind in moves:
        target_dir = folder / kind
        target_dir.mkdir(exist_ok=True)
        final_name = _unique_target(target_dir, name)
        (folder / name).rename(target_dir / final_name)
        recorded.append((name, kind, final_name))
    (folder / "undo.json").write_text(json.dumps(recorded), encoding="utf-8")
    return [(name, kind) for name, kind, _ in recorded]


def undo(folder: Path) -> list[tuple[str, str]]:
    payload = json.loads((folder / "undo.json").read_text(encoding="utf-8"))
    restored: list[tuple[str, str]] = []
    for entry in payload:
        if len(entry) == 3:
            original, kind, final_name = entry
        else:
            original, kind = entry
            final_name = original
        source = folder / kind / final_name
        if source.exists():
            source.rename(folder / original)
        restored.append((original, kind))
    return restored


def summary(folder: Path) -> dict[str, int]:
    return dict(Counter(kind for _, kind in plan(folder)))
