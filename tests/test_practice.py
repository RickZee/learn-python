"""Every practice notebook must pass with its reference solution, and must fail
cleanly (NotImplementedError or AssertionError) as shipped.

The reference solution is solutions/<same folder>/<name>.py. Its top-level
functions and classes replace the same-named stubs in the notebook. An exercise
that is not function-shaped can instead ship a fully solved copy at
solutions/<same folder>/<name>.ipynb, which runs as-is.
"""

from __future__ import annotations

import ast
import pathlib

import nbformat
import pytest

from tests.notebook_runner import execute_notebook

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-practice.ipynb",
    "patterns/*/*-practice.ipynb",
    "challenges/problems/*.ipynb",
)
PRACTICE = sorted(p for pattern in PATTERNS for p in ROOT.glob(pattern))
CLEAN_FAILURES = {"NotImplementedError", "AssertionError"}
DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def solution_for(notebook: pathlib.Path) -> pathlib.Path:
    rel = notebook.relative_to(ROOT)
    stem = rel.name.removesuffix(".ipynb").removesuffix("-practice")
    return ROOT / "solutions" / rel.parent / f"{stem}.py"


def top_level_defs(source: str) -> dict[str, str]:
    """Map each top-level def/class name to its source, including decorators."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    found: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, DEFS):
            continue
        start = (node.decorator_list[0].lineno if node.decorator_list else node.lineno) - 1
        found[node.name] = "".join(lines[start : node.end_lineno]).rstrip()
    return found


def splice(cell_source: str, solution: dict[str, str]) -> str:
    """Replace each top-level def/class that the solution also defines."""
    tree = ast.parse(cell_source)
    lines = cell_source.splitlines(keepends=True)
    targets = [node for node in tree.body if isinstance(node, DEFS) and node.name in solution]
    for node in sorted(targets, key=lambda item: item.lineno, reverse=True):
        start = (node.decorator_list[0].lineno if node.decorator_list else node.lineno) - 1
        lines[start : node.end_lineno] = [solution[node.name] + "\n"]
    return "".join(lines)


def first_error(nb: nbformat.NotebookNode, path: pathlib.Path) -> str | None:
    execute_notebook(nb, path, allow_errors=True)
    for cell in nb.cells:
        for out in cell.get("outputs", []):
            if out.output_type == "error":
                return f"{out.ename}: {out.evalue}"
    return None


def ids(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT))


@pytest.mark.parametrize("path", PRACTICE, ids=ids)
def test_reference_solution_passes(path: pathlib.Path) -> None:
    sol = solution_for(path)
    solved_notebook = sol.with_suffix(".ipynb")
    if solved_notebook.exists():  # for exercises that are not function-shaped
        assert first_error(nbformat.read(solved_notebook, as_version=4), path) is None
        return
    assert sol.exists(), f"missing reference solution: {sol.relative_to(ROOT)}"
    solution = top_level_defs(sol.read_text(encoding="utf-8"))
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = splice(cell.source, solution)
    assert first_error(nb, path) is None


@pytest.mark.parametrize("path", PRACTICE, ids=ids)
def test_unsolved_notebook_fails_cleanly(path: pathlib.Path) -> None:
    nb = nbformat.read(path, as_version=4)
    error = first_error(nb, path)
    assert error is not None, "the unsolved notebook passes; the checks test nothing"
    assert error.split(":")[0] in CLEAN_FAILURES, f"confusing failure for a learner: {error}"
