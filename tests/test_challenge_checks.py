"""Challenge notebooks have enough checks, including a random cross-check."""

from __future__ import annotations

import ast
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "challenges" / "problems"
WORD = re.compile(r"[A-Za-z0-9']+")
RANDOM = re.compile(r"\brandom\b")
GENERIC_EXCUSE = "compact brute oracle is not required"
MINIMUM_CHECKS = 8
MINIMUM_REASON_WORDS = 8
NOTEBOOKS = sorted(PROBLEMS.glob("*.ipynb"))


def _cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else source


def _checks(source: str) -> int:
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            count += 1
            continue
        called = isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        if called and node.func.id == "check":
            count += 1
    return count


def _random_cross_check(notebook: dict) -> str | None:
    """Return an error string, or None when the notebook explains itself."""
    saw_random = False
    saw_no_random = False
    for cell in notebook["cells"]:
        tags = cell.get("metadata", {}).get("tags") or []
        text = _cell_text(cell)
        if "no-random" in tags:
            saw_no_random = True
            if cell.get("cell_type") != "markdown":
                return "tag no-random on a markdown cell and state why randomization does not fit"
            if len(WORD.findall(text)) < MINIMUM_REASON_WORDS:
                return "the no-random cell needs a reason of at least 8 words"
            if GENERIC_EXCUSE in text:
                return (
                    "no-random reason is the banned generic excuse; "
                    "add a real oracle or a specific reason"
                )
        if cell.get("cell_type") == "code" and RANDOM.search(text):
            saw_random = True
    if saw_no_random:
        return None
    if saw_random:
        return None
    return "needs a randomized cross-check, or a markdown cell tagged no-random that says why"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda path: path.name)
def test_notebook_has_enough_checks(path: pathlib.Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    total = 0
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        total += _checks(_cell_text(cell))
    assert total >= MINIMUM_CHECKS, f"{total} checks; need {MINIMUM_CHECKS}"
    reason = _random_cross_check(notebook)
    assert reason is None, reason
