"""Every challenge solution has a walkthrough with the required sections."""

from __future__ import annotations

import pathlib
import re

import pytest

from tests._text import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOLUTIONS = ROOT / "solutions" / "challenges" / "problems"
WORD = re.compile(r"[A-Za-z0-9']+")
FENCE = re.compile(r"```.*?```", re.DOTALL)
HEADINGS = (
    "Recognize it",
    "Brute force",
    "Key insight",
    "Algorithm",
    "Trace",
    "Complexity",
    "Edge cases",
    "Alternatives and trade-offs",
    "Common bugs",
    "Follow-ups",
    "Related problems",
)
BANNED_PHRASES = (
    "Name the pattern before coding",
    "Keep an invariant that makes each step",
    "Initialize the structure named",
    "Neighboring notebooks",
    "Enumerate combinations or scan naively until the cost is clear",
)
MINIMUM_WORDS = 350
SOLUTION_FILES = sorted(SOLUTIONS.glob("*.py"))


def _headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def _in_order(found: list[str]) -> bool:
    index = 0
    for required in HEADINGS:
        while index < len(found) and found[index] != required:
            index += 1
        if index == len(found):
            return False
        index += 1
    return True


@pytest.mark.parametrize("path", SOLUTION_FILES, ids=lambda path: path.name)
def test_solution_has_a_walkthrough(path: pathlib.Path) -> None:
    writeup = path.with_suffix(".md")
    assert writeup.is_file(), f"missing walkthrough {writeup.relative_to(ROOT)}"
    text = writeup.read_text(encoding="utf-8")
    found = _headings(text)
    assert _in_order(found), f"headings out of order or missing: {found}"
    words = len(WORD.findall(FENCE.sub(" ", text)))
    assert words >= MINIMUM_WORDS, f"walkthrough has {words} words; need {MINIMUM_WORDS}"
    normalized = normalize(text)
    banned = [phrase for phrase in BANNED_PHRASES if normalize(phrase) in normalized]
    assert not banned, "template phrases: " + "; ".join(banned)
