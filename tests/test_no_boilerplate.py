"""A long sentence copied across many lessons is boilerplate.

A sentence of 10 or more words that shows up in more than three lesson
notebooks fails, unless it is listed in tests/boilerplate_allowlist.txt.
That file holds structural prompts only, at most 10, and each entry must
itself be one of those repeated sentences.
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOW = ROOT / "tests" / "boilerplate_allowlist.txt"
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "patterns/*/*-lesson.ipynb",
    "internals/*/*-lesson.ipynb",
)
WORD = re.compile(r"[A-Za-z0-9']+")
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
CODE = re.compile(r"`[^`]*`")
TAG = re.compile(r"<[^>]+>")
FENCE = re.compile(r"```.*?```", re.DOTALL)
HEADING = re.compile(r"^#{1,6}\s*", re.MULTILINE)
LIMIT = 10
MINIMUM_WORDS = 10
MAXIMUM_NOTEBOOKS = 3


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
            found.setdefault(sentence, set()).add(rel)
    return {
        sentence: paths
        for sentence, paths in found.items()
        if len(paths) > MAXIMUM_NOTEBOOKS
    }


def allowlist() -> list[str]:
    lines = []
    for line in ALLOW.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return lines


def test_allowlist_is_short_and_names_real_repeats() -> None:
    allowed = allowlist()
    assert len(allowed) <= LIMIT, f"allowlist has {len(allowed)} sentences; the cap is {LIMIT}"
    assert len(allowed) == len(set(allowed)), "allowlist repeats a sentence"
    repeats = repeated_sentences()
    for sentence in allowed:
        assert sentence in repeats, (
            "allowlist entry is not a sentence copied across more than three lessons: "
            + sentence
        )


def test_long_sentences_are_not_copied_across_lessons() -> None:
    allowed = set(allowlist())
    copied = {
        sentence: paths
        for sentence, paths in repeated_sentences().items()
        if sentence not in allowed
    }
    details = "\n".join(
        f"{sentence}\n  " + "\n  ".join(sorted(paths))
        for sentence, paths in sorted(copied.items())
    )
    assert not copied, "boilerplate sentences:\n" + details
