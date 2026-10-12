"""Print lesson word counts against the tier ranges.

Words are counted in markdown cells only. Fenced code blocks are excluded.
A lesson with no **Tier:** tag is reported as untagged and LOW.

Usage:
    uv run python tools/depth_report.py            # every lesson
    uv run python tools/depth_report.py PATH ...   # just these notebooks
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "patterns/*/*-lesson.ipynb",
    "internals/*/*-lesson.ipynb",
)
WORD = re.compile(r"[A-Za-z0-9']+")
TIER = re.compile(r"\*\*Tier:\*\*\s*(Core|Intermediate|Deep)\b")
FENCE = re.compile(r"```.*?```", re.DOTALL)
RANGES = {
    "Core": (350, 600),
    "Intermediate": (600, 1000),
    "Deep": (900, 1600),
}


def _cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else source


def lessons(args: list[str]) -> list[Path]:
    if not args:
        return sorted(path for pattern in PATTERNS for path in ROOT.glob(pattern))
    found: list[Path] = []
    for arg in args:
        path = Path(arg)
        if not path.is_absolute():
            path = ROOT / path
        if path.is_dir():
            found.extend(sorted(path.rglob("*-lesson.ipynb")))
        else:
            found.append(path)
    return found


def words_outside_code(notebook: dict) -> int:
    total = 0
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        text = FENCE.sub(" ", _cell_text(cell))
        total += len(WORD.findall(text))
    return total


def tier_of(notebook: dict) -> str | None:
    if not notebook["cells"]:
        return None
    match = TIER.search(_cell_text(notebook["cells"][0]))
    return match.group(1) if match else None


def judge(tier: str | None, count: int) -> tuple[str, str, str]:
    if tier not in RANGES:
        return "untagged", "-", "LOW"
    low, high = RANGES[tier]
    if count < low:
        status = "LOW"
    elif count > high:
        status = "HIGH"
    else:
        status = "OK"
    return tier, f"{low}–{high}", status


def rows(paths: list[Path]) -> list[tuple[str, str, int, str, str]]:
    table = []
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        count = words_outside_code(notebook)
        tier, span, status = judge(tier_of(notebook), count)
        rel = path.resolve().relative_to(ROOT).as_posix()
        table.append((rel, tier, count, span, status))
    return table


def render(table: list[tuple[str, str, int, str, str]]) -> str:
    header = "| lesson | tier | words | range | status |"
    rule = "|---|---|---:|---|---|"
    lines = [header, rule]
    for path, tier, count, span, status in table:
        lines.append(f"| {path} | {tier} | {count} | {span} | {status} |")
    counts = {status: 0 for status in ("OK", "LOW", "HIGH")}
    for *_, status in table:
        counts[status] = counts.get(status, 0) + 1
    lines.append("")
    lines.append(
        f"{len(table)} lessons: {counts['OK']} OK, {counts['LOW']} LOW, {counts['HIGH']} HIGH"
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    print(render(rows(lessons(argv))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
