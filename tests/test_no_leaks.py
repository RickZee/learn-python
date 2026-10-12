"""Pattern lessons must not contain a challenge problem's functions or asserts."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _sources(folder: Path) -> list[str]:
    chunks: list[str] = []
    for path in sorted(folder.rglob("*")):
        if path.suffix == ".py":
            chunks.append(path.read_text(encoding="utf-8"))
        elif path.suffix == ".ipynb":
            notebook = json.loads(path.read_text(encoding="utf-8"))
            for cell in notebook["cells"]:
                if cell.get("cell_type") == "code":
                    chunks.append("".join(cell.get("source", [])))
    return chunks


def _names(chunks: list[str]) -> set[str]:
    found: set[str] = set()
    for source in chunks:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                found.add(node.name)
    return found


def _asserts(chunks: list[str]) -> set[str]:
    found: set[str] = set()
    for source in chunks:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                segment = ast.get_source_segment(source, node.test)
                if segment:
                    found.add(" ".join(segment.split()))
    return found


def test_patterns_do_not_define_challenge_functions() -> None:
    pattern_names = _names(_sources(ROOT / "patterns") + _sources(ROOT / "solutions" / "patterns"))
    challenge_names = _names(
        _sources(ROOT / "challenges" / "problems")
        + _sources(ROOT / "solutions" / "challenges" / "problems")
    )
    shared = sorted(pattern_names & challenge_names)
    assert not shared, "challenge names leaked into patterns: " + ", ".join(shared)


def test_patterns_do_not_copy_challenge_asserts() -> None:
    pattern_asserts = _asserts(_sources(ROOT / "patterns"))
    challenge_asserts = _asserts(_sources(ROOT / "challenges" / "problems"))
    shared = sorted(pattern_asserts & challenge_asserts)
    assert not shared, "challenge asserts leaked into patterns:\n" + "\n".join(shared)


def _normalize_body(node: ast.AST) -> str:
    """Drop names that differ but keep control-flow shape of a function body."""
    class Strip(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.Name:
            return ast.copy_location(ast.Name(id="N", ctx=node.ctx), node)

        def visit_arg(self, node: ast.arg) -> ast.arg:
            return ast.copy_location(ast.arg(arg="a", annotation=None), node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
            self.generic_visit(node)
            node.name = "f"
            node.decorator_list = []
            node.returns = None
            return node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
            self.generic_visit(node)
            node.name = "f"
            node.decorator_list = []
            node.returns = None
            return node

        def visit_Constant(self, node: ast.Constant) -> ast.Constant:
            if isinstance(node.value, str):
                return ast.copy_location(ast.Constant(value="S"), node)
            if isinstance(node.value, (int, float)):
                return ast.copy_location(ast.Constant(value=0), node)
            return node

    cleaned = Strip().visit(node)
    ast.fix_missing_locations(cleaned)
    return ast.dump(cleaned, include_attributes=False)


def _function_bodies(chunks: list[str]) -> dict[str, str]:
    bodies: dict[str, str] = {}
    for source in chunks:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                bodies[node.name] = _normalize_body(node)
    return bodies


def test_pattern_bodies_do_not_match_challenge_solutions() -> None:
    """A pattern lesson must not paste a challenge solution body (AST shape)."""
    pattern_bodies = _function_bodies(
        _sources(ROOT / "patterns") + _sources(ROOT / "solutions" / "patterns")
    )
    challenge_bodies = _function_bodies(
        _sources(ROOT / "challenges" / "problems")
        + _sources(ROOT / "solutions" / "challenges" / "problems")
    )
    # Compare by normalized body dump, not by name (names already checked).
    challenge_dumps = set(challenge_bodies.values())
    leaks = sorted(
        name
        for name, body in pattern_bodies.items()
        if body in challenge_dumps and len(body) > 80  # ignore tiny stubs
    )
    assert not leaks, "pattern function bodies match challenge solutions: " + ", ".join(leaks)

