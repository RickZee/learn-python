"""Challenge notebooks have enough real checks (G6) and a random cross-check."""

from __future__ import annotations

import ast
import json
import pathlib
import re

import pytest

from tests._text import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "challenges" / "problems"
WORD = re.compile(r"[A-Za-z0-9']+")
RANDOM = re.compile(r"\brandom\b")
GENERIC_EXCUSE = "compact brute oracle is not required"
BANNED_NO_RANDOM = ("not required", "this round")
MINIMUM_CHECKS = 8
MINIMUM_REASON_WORDS = 8
NOTEBOOKS = sorted(PROBLEMS.glob("*.ipynb"))
ORACLE_PREFIXES = ("brute", "slow", "ref", "oracle")
HELPER_NAMES = {
    "listnode",
    "treenode",
    "node",
    "interval",
    "nodes",
    "values",
    "to list",
    "from list",
}


def _cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else source


def _is_const(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(_is_const(elt) for elt in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub, ast.Not)):
        return _is_const(node.operand)
    return False


def _is_constant_assert(node: ast.Assert) -> bool:
    test = node.test
    if isinstance(test, ast.Constant):
        return True
    if isinstance(test, ast.Compare):
        return _is_const(test.left) and all(_is_const(c) for c in test.comparators)
    return False


def _assert_calls_name(node: ast.Assert, names: set[str]) -> bool:
    class_names = {n for n in names if n[:1].isupper()}
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name) and func.id in names:
                return True
            if (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id in names
            ):
                return True
            # Method call on an instance variable for a class under test
            if class_names and isinstance(func, ast.Attribute):
                return True
    return False


def _stub_names(notebook: dict) -> set[str]:
    names: set[str] = set()
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        try:
            tree = ast.parse(_cell_text(cell))
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                n = normalize(node.name)
                if node.name.startswith("_") or any(n.startswith(p) for p in ORACLE_PREFIXES):
                    continue
                if n in HELPER_NAMES:
                    continue
                names.add(node.name)
    return names


def _real_check_count(source: str, stubs: set[str]) -> tuple[int, bool]:
    """Return (count, has_constant_assert)."""
    tree = ast.parse(source)
    count = 0
    has_constant = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            if _is_constant_assert(node):
                has_constant = True
                continue
            if stubs and _assert_calls_name(node, stubs) or not stubs:
                count += 1
            continue
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"cross_check", "cross_check_ops", "check"}
        ):
            count += 1
    return count, has_constant


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
            normalized = normalize(text)
            if normalize(GENERIC_EXCUSE) in normalized:
                return (
                    "no-random reason is the banned generic excuse; "
                    "add a real oracle or a specific reason"
                )
            for banned in BANNED_NO_RANDOM:
                if normalize(banned) in normalized:
                    return f"no-random reason bans '{banned}'"
        if cell.get("cell_type") == "code" and RANDOM.search(text):
            saw_random = True
        if cell.get("cell_type") == "code" and (
            "cross_check(" in text or "cross_check_ops(" in text
        ):
            saw_random = True
    if saw_no_random:
        return None
    if saw_random:
        return None
    return "needs a randomized cross-check, or a markdown cell tagged no-random that says why"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda path: path.name)
def test_notebook_has_enough_checks(path: pathlib.Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    stubs = _stub_names(notebook)
    total = 0
    has_constant = False
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = _cell_text(cell)
        try:
            count, const = _real_check_count(source, stubs)
        except SyntaxError:
            continue
        total += count
        has_constant = has_constant or const
    assert not has_constant, "constant asserts are banned (D3)"
    assert total >= MINIMUM_CHECKS, f"{total} real checks; need {MINIMUM_CHECKS}"
    reason = _random_cross_check(notebook)
    assert reason is None, reason
