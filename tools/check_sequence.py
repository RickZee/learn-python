"""Fail when a course notebook uses a concept before its lesson.

Usage: uv run python tools/check_sequence.py
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "maintainers" / "concepts.md"

NODE_CONCEPTS = {
    "If": "conditions",
    "IfExp": "conditions",
    "For": "loops",
    "While": "loops",
    "FunctionDef": "functions-basic",
    "Return": "functions-basic",
    "ClassDef": "classes",
    "ListComp": "comprehensions",
    "DictComp": "comprehensions",
    "SetComp": "comprehensions",
    "GeneratorExp": "comprehensions",
    "Try": "exceptions",
    "Raise": "raise",
    "With": "with",
    "Lambda": "lambda",
    "Match": "match",
    "Yield": "generators",
    "YieldFrom": "generators",
    "AsyncFunctionDef": "async",
    "Await": "async",
    "JoinedStr": "f-strings",
}


def introduced() -> dict[str, str]:
    found: dict[str, str] = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| Concept") or line.startswith("| ---"):
            continue
        cells = [part.strip() for part in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and cells[1].endswith(".ipynb"):
            found[cells[0]] = cells[1]
    return found


def _not_implemented(node: ast.Raise) -> bool:
    exc = node.exc
    if isinstance(exc, ast.Name):
        return exc.id == "NotImplementedError"
    if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
        return exc.func.id == "NotImplementedError"
    return False


def concepts_in(source: str) -> set[str]:
    tree = ast.parse(source)
    found: set[str] = set()
    for node in ast.walk(tree):
        name = type(node).__name__
        if name == "Raise" and isinstance(node, ast.Raise) and _not_implemented(node):
            continue
        if name in NODE_CONCEPTS:
            found.add(NODE_CONCEPTS[name])
        decorated = isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        if decorated and node.decorator_list:
            found.add("decorators")
        if isinstance(node, ast.Starred):
            found.add("star-args")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
            node.args.vararg or node.args.kwarg or node.args.kwonlyargs
        ):
            found.add("star-args")
    return found


def violations() -> list[str]:
    intro = introduced()
    problems: list[str] = []
    for path in sorted(ROOT.joinpath("course").rglob("*.ipynb")):
        rel = path.relative_to(ROOT).as_posix()
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for index, cell in enumerate(notebook["cells"]):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            if source.lstrip().startswith(("%", "!")):
                continue
            try:
                used = concepts_in(source)
            except SyntaxError:
                continue
            for concept in sorted(used):
                where = intro.get(concept)
                if where is None:
                    problems.append(
                        f"{rel} cell {index} uses {concept}, "
                        "which is not in docs/maintainers/concepts.md"
                    )
                elif where > rel:
                    problems.append(f"{rel} cell {index} uses {concept} before {where}")
    return problems


def main() -> None:
    found = violations()
    if found:
        print("\n".join(found))
        sys.exit(1)
    print("sequence ok")


if __name__ == "__main__":
    main()
