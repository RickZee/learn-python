"""Practice notebooks: no hint leaks (G8) and Warm-up→…→Reflect shape (G9)."""

from __future__ import annotations

import ast
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PRACTICES = sorted(
    list(ROOT.glob("course/*/*-practice.ipynb")) + list(ROOT.glob("patterns/*/*-practice.ipynb"))
)
FENCE = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)
INLINE = re.compile(r"`([^`\n]+)`")
HEADING = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def _cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else source


def _solution_path(practice: pathlib.Path) -> pathlib.Path | None:
    rel = practice.relative_to(ROOT)
    # course/04-collections/03-dicts-practice.ipynb → solutions/course/04-collections/03-dicts.py
    name = practice.name.replace("-practice.ipynb", ".py")
    candidate = ROOT / "solutions" / rel.parent / name
    return candidate if candidate.is_file() else None


def _function_bodies(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    bodies: list[str] = []
    lines = source.splitlines()
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        # body without def line; drop docstring
        start = node.body[0].lineno - 1
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(getattr(node.body[0], "value", None), ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            if len(node.body) == 1:
                continue
            start = node.body[1].lineno - 1
        end = node.end_lineno or start + 1
        chunk = "\n".join(lines[start:end])
        compact = re.sub(r"\s+", "", chunk)
        if len(compact) >= 12:
            bodies.append(compact)
    return bodies


def _hint_code_snippets(markdown: str) -> list[str]:
    snippets: list[str] = []
    for block in FENCE.findall(markdown):
        compact = re.sub(r"\s+", "", block)
        if compact:
            snippets.append(compact)
    for piece in INLINE.findall(markdown):
        compact = re.sub(r"\s+", "", piece)
        if compact:
            snippets.append(compact)
    return snippets


def _headings(nb: dict) -> list[str]:
    found: list[str] = []
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        for match in HEADING.finditer(_cell_text(cell)):
            found.append(match.group(1).strip())
    return found


def _stmt_count(func: ast.AST) -> int:
    assert isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef))
    body = list(func.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(getattr(body[0], "value", None), ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    count = 0
    for node in body:
        count += sum(1 for child in ast.walk(node) if isinstance(child, ast.stmt))
    return count


def _core_or_stretch_large_enough(solution: pathlib.Path) -> bool:
    source = solution.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _stmt_count(node) >= 4:
            return True
    return False


@pytest.mark.parametrize("path", PRACTICES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_g8_hints_do_not_leak_solutions(path: pathlib.Path) -> None:
    solution = _solution_path(path)
    if solution is None:
        return
    bodies = _function_bodies(solution.read_text(encoding="utf-8"))
    if not bodies:
        return
    nb = json.loads(path.read_text(encoding="utf-8"))
    markdown = "\n".join(_cell_text(c) for c in nb["cells"] if c.get("cell_type") == "markdown")
    for snippet in _hint_code_snippets(markdown):
        for body in bodies:
            assert snippet != body and body not in snippet, (
                "hint contains a reference-solution body"
            )


@pytest.mark.parametrize("path", PRACTICES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_g9_practice_shape(path: pathlib.Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    nb = json.loads(path.read_text(encoding="utf-8"))
    headings = _headings(nb)
    required = ["Warm-up", "Core"]
    needs_debug = True
    if rel.startswith("course/00-start/") or rel.startswith("course/01-basics/"):
        needs_debug = False
    if rel.startswith("patterns/"):
        needs_debug = False  # pattern practices: Debug not required by D9 (from 02-strings)
    if needs_debug:
        required.append("Debug")
    required.extend(["Stretch", "Reflect"])
    positions: list[int] = []
    for name in required:
        assert name in headings, f"missing ## {name}"
        positions.append(headings.index(name))
    assert positions == sorted(positions), "practice headings out of order"

    if rel.startswith("course/00-start/"):
        return
    if rel.startswith("patterns/"):
        return
    # From 01-basics on: Core or Stretch reference body ≥ 4 statements
    solution = _solution_path(path)
    assert solution is not None, f"missing solution for {rel}"
    assert _core_or_stretch_large_enough(solution), (
        "Core or Stretch reference body needs ≥ 4 statements"
    )
