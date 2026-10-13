"""Challenge notebooks: statement, hints, stub, no oracles, walkthrough link (G1–G5, G7)."""

from __future__ import annotations

import ast
import json
import pathlib
import re

import pytest

from tests._text import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBLEMS = sorted((ROOT / "challenges" / "problems").glob("*.ipynb"))
WORD = re.compile(r"[A-Za-z0-9']+")
BANNED_G2 = (
    "solve the stub",
    "lesson prompt",
    "padding asserts",
    "asserts encode examples",
    "edges follow in the same cell",
    "see asserts for",
    "see the walkthrough",
)
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
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def _cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else source


def _load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _markdown(nb: dict) -> str:
    return "\n".join(_cell_text(c) for c in nb["cells"] if c.get("cell_type") == "markdown")


def _strip_fences(text: str) -> str:
    return re.sub(r"```.*?```", " ", text, flags=re.DOTALL)


def _is_oracle_name(name: str) -> bool:
    n = normalize(name)
    return any(n == p or n.startswith(p) for p in ORACLE_PREFIXES)


@pytest.mark.parametrize("path", PROBLEMS, ids=lambda p: p.name)
def test_g1_statement(path: pathlib.Path) -> None:
    first = _cell_text(_load(path)["cells"][0])
    prose = _strip_fences(first)
    words = len(WORD.findall(prose))
    assert words >= 60, f"first cell has {words} words; need ≥ 60"
    assert "**Difficulty:**" in first
    assert "**Target:**" in first
    assert "**Constraints.**" in first
    assert "**Pattern:**" not in first
    assert "Solutions:" not in first


@pytest.mark.parametrize("path", PROBLEMS, ids=lambda p: p.name)
def test_g2_no_template_text(path: pathlib.Path) -> None:
    md = _strip_fences(_markdown(_load(path)))
    # Link targets may name the walkthrough file; only prose is checked for the slug.
    prose = LINK.sub(r"\1", md)
    normalized = normalize(prose)
    for phrase in BANNED_G2:
        assert normalize(phrase) not in normalized, f"banned phrase: {phrase}"
    assert path.stem not in prose, f"problem slug {path.stem!r} appears in prose"


@pytest.mark.parametrize("path", PROBLEMS, ids=lambda p: p.name)
def test_g3_hints(path: pathlib.Path) -> None:
    md = _markdown(_load(path))
    assert "## Hints" in md, "missing ## Hints"
    part = md.split("## Hints", 1)[1]
    part = re.split(r"\n## ", part, maxsplit=1)[0]
    details = re.findall(r"<details\b[^>]*>.*?</details>", part, flags=re.I | re.S)
    assert len(details) >= 3, f"{len(details)} hint details; need ≥ 3"
    last = details[-1]
    assert "```" in last and "___" in last, "last hint needs a code fence with ___"


@pytest.mark.parametrize("path", PROBLEMS, ids=lambda p: p.name)
def test_g4_typed_stub(path: pathlib.Path) -> None:
    nb = _load(path)
    has_star = False
    typed_public = False
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        try:
            tree = ast.parse(_cell_text(cell))
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.args.vararg or node.args.kwarg:
                    has_star = True
                if node.name.startswith("_") or _is_oracle_name(node.name):
                    continue
                if normalize(node.name) in HELPER_NAMES:
                    continue
                args = [a for a in node.args.args if a.arg != "self"]
                if node.returns is not None and all(a.annotation is not None for a in args):
                    typed_public = True
            elif isinstance(node, ast.ClassDef):
                if node.name.startswith("_") or _is_oracle_name(node.name):
                    continue
                if normalize(node.name) in HELPER_NAMES:
                    continue
                typed_public = True
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and (item.args.vararg or item.args.kwarg):
                        has_star = True
    assert not has_star, "learner code must not use *args, **kwargs"
    assert typed_public, "stub must be typed (annotated public function or class)"


@pytest.mark.parametrize("path", PROBLEMS, ids=lambda p: p.name)
def test_g5_no_oracles(path: pathlib.Path) -> None:
    nb = _load(path)
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        try:
            tree = ast.parse(_cell_text(cell))
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                assert not _is_oracle_name(node.name), f"oracle name in learner file: {node.name}"
    has_random = any(
        cell.get("cell_type") == "code" and "random.Random" in _cell_text(cell)
        for cell in nb["cells"]
    )
    has_prop = any(
        "property-check" in (cell.get("metadata", {}).get("tags") or []) for cell in nb["cells"]
    )
    assert not has_random or has_prop, "random.Random needs a markdown cell tagged property-check"


@pytest.mark.parametrize("path", PROBLEMS, ids=lambda p: p.name)
def test_g7_walkthrough_link(path: pathlib.Path) -> None:
    nb = _load(path)
    want = f"solutions/challenges/problems/{path.stem}.md"
    solution_links: list[tuple[str, str]] = []
    # Track which section each link is in
    section = ""
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        text = _cell_text(cell)
        for line in text.splitlines():
            if line.startswith("## "):
                section = line[3:].strip()
            for _, href in LINK.findall(line):
                target = href.split("#", 1)[0]
                if "solutions/" in target:
                    solution_links.append((section, target))
    assert solution_links, "missing walkthrough link under ## After you pass"
    for section, target in solution_links:
        assert section == "After you pass", (
            f"solutions link only allowed under ## After you pass, found in {section!r}"
        )
        assert target.endswith(want) or want in target or target.endswith(f"{path.stem}.md"), (
            f"walkthrough link should point at {want}, got {target}"
        )
