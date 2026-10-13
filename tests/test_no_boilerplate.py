"""Boilerplate sentences (G13) and constant asserts (G14)."""

from __future__ import annotations

import ast
import json
import pathlib
import re

import pytest

from tests._status import pending
from tests._text import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOW = ROOT / "tests" / "boilerplate_allowlist.txt"
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "course/*/*-practice.ipynb",
    "patterns/*/*-lesson.ipynb",
    "patterns/*/*-practice.ipynb",
    "internals/*/*-lesson.ipynb",
    "challenges/problems/*.ipynb",
)
LEARNER_NOTEBOOKS = (
    "course/*/*.ipynb",
    "patterns/*/*.ipynb",
    "internals/*/*.ipynb",
    "challenges/problems/*.ipynb",
    "use-cases/*/*.ipynb",
)
WORD = re.compile(r"[A-Za-z0-9']+")
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
CODE = re.compile(r"`[^`]*`")
TAG = re.compile(r"<[^>]+>")
FENCE = re.compile(r"```.*?```", re.DOTALL)
HEADING = re.compile(r"^#{1,6}\s*", re.MULTILINE)
LIMIT = 10
MINIMUM_WORDS = 10
MAXIMUM_NOTEBOOKS = 2


def _cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else source


def _prose(markdown: str) -> str:
    text = FENCE.sub(" ", markdown)
    text = CODE.sub(" ", text)
    text = LINK.sub(r"\1", text)
    text = TAG.sub(" ", text)
    text = HEADING.sub("", text)
    return text


def sentences(markdown: str) -> list[str]:
    """Sentences of at least 10 words, after markdown is stripped to prose."""
    found: list[str] = []
    for block in re.split(r"\n\s*\n", _prose(markdown)):
        flat = " ".join(block.split())
        for part in re.split(r"(?<=[.!?])\s+", flat):
            sentence = part.strip()
            if len(WORD.findall(sentence)) >= MINIMUM_WORDS:
                found.append(sentence)
    return found


def lesson_paths() -> list[pathlib.Path]:
    return sorted(path for pattern in PATTERNS for path in ROOT.glob(pattern))


def repeated_sentences() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for path in lesson_paths():
        notebook = json.loads(path.read_text(encoding="utf-8"))
        markdown = "\n\n".join(
            _cell_text(cell) for cell in notebook["cells"] if cell.get("cell_type") == "markdown"
        )
        rel = path.relative_to(ROOT).as_posix()
        for sentence in sentences(markdown):
            key = normalize(sentence)
            found.setdefault(key, set()).add(rel)
    return {sentence: paths for sentence, paths in found.items() if len(paths) > MAXIMUM_NOTEBOOKS}


def allowlist() -> list[str]:
    lines = []
    for line in ALLOW.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return lines


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


def test_allowlist_is_short_and_names_real_repeats() -> None:
    allowed = allowlist()
    assert len(allowed) <= LIMIT, f"allowlist has {len(allowed)} sentences; the cap is {LIMIT}"
    assert len(allowed) == len(set(allowed)), "allowlist repeats a sentence"
    repeats = repeated_sentences()
    for sentence in allowed:
        assert normalize(sentence) in repeats, (
            "allowlist entry is not a sentence copied across more than two notebooks: " + sentence
        )


def test_long_sentences_are_not_copied_across_lessons() -> None:
    allowed = {normalize(sentence) for sentence in allowlist()}
    copied = {
        sentence: paths
        for sentence, paths in repeated_sentences().items()
        if sentence not in allowed
    }
    pending_paths = pending("G13")
    involved = set().union(*copied.values()) if copied else set()
    stale = pending_paths - involved
    assert not stale, "G13 paths no longer in a banned repeat; remove them:\n" + "\n".join(
        sorted(stale)
    )
    if copied and involved <= pending_paths:
        pytest.xfail("listed under G13 in docs/maintainers/status.md")
    details = "\n".join(
        f"{sentence}\n  " + "\n  ".join(sorted(paths)) for sentence, paths in sorted(copied.items())
    )
    assert not copied, "boilerplate sentences:\n" + details


def _has_constant_assert(path: pathlib.Path) -> bool:
    if path.suffix == ".py":
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            return False
        return any(
            isinstance(node, ast.Assert) and _is_constant_assert(node) for node in ast.walk(tree)
        )
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        try:
            tree = ast.parse(_cell_text(cell))
        except SyntaxError:
            continue
        if any(
            isinstance(node, ast.Assert) and _is_constant_assert(node) for node in ast.walk(tree)
        ):
            return True
    return False


def _learner_paths() -> list[pathlib.Path]:
    found = [path for pattern in LEARNER_NOTEBOOKS for path in ROOT.glob(pattern)]
    found.extend(ROOT.glob("course/*/exercise/*.py"))
    return sorted(found)


@pytest.mark.parametrize(
    "path",
    _learner_paths(),
    ids=lambda p: p.relative_to(ROOT).as_posix(),
)
def test_g14_no_constant_asserts(path: pathlib.Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    broken = _has_constant_assert(path)
    if broken and rel in pending("G14"):
        pytest.xfail("listed under G14 in docs/maintainers/status.md")
    if broken:
        pytest.fail(f"constant assert in {rel}")
    if rel in pending("G14"):
        pytest.fail(f"{rel} is listed under G14 but has no constant assert; remove it")
