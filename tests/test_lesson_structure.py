"""Lessons keep the depth sections and the teach-first lesson flow."""

from __future__ import annotations

import json
import pathlib
import re

import pytest

from tests._status import pending
from tests._text import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "patterns/*/*-lesson.ipynb",
    "internals/*/*-lesson.ipynb",
)
LESSONS = sorted(path for pattern in PATTERNS for path in ROOT.glob(pattern))
WORD = re.compile(r"[A-Za-z0-9']+")
TIER = re.compile(r"\*\*Tier:\*\*\s*(Core|Intermediate|Deep)\b")
USES = re.compile(r"\*\*Uses:\*\*[^\n]*")
MISTAKE = re.compile(r"^##\s+.*(common mistake|real mistake)", re.IGNORECASE | re.MULTILINE)
PREDICT_HEADING = re.compile(r"^##\s+Predict\b", re.MULTILINE)
FIRST_WHY = "Why you'd use this"
FIRST_GOALS = "After this lesson you can"
COURSE_FLOW = [
    "Quick review",
    "The idea",
    "See it work",
    "Check yourself",
    "Why it works this way",
    "When to use it",
    "Common mistake",
    "Try it",
    "Recap",
]
FIRST_COURSE_LESSON = "course/00-start/01-first-program-lesson.ipynb"


def _text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def _sections(cells: list[dict]) -> list[tuple[str, str]]:
    title: str | None = None
    parts: list[str] = []
    found: list[tuple[str, str]] = []

    def flush() -> None:
        nonlocal title, parts
        if title is not None:
            found.append((title, "\n".join(parts)))
        title = None
        parts = []

    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        lines = _text(cell).splitlines()
        index = 0
        while index < len(lines):
            line = lines[index]
            if line.startswith("## "):
                flush()
                title = line[3:].strip()
                rest = "\n".join(lines[index + 1 :]).strip()
                if rest:
                    parts.append(rest)
                break
            if title is not None and line.strip():
                parts.append(line)
            index += 1
        else:
            body = _text(cell).strip()
            if title is not None and body:
                parts.append(body)
    flush()
    return found


def _headings(cells: list[dict]) -> list[str]:
    found: list[str] = []
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        for line in _text(cell).splitlines():
            if line.startswith("## "):
                found.append(line[3:].strip())
    return found


def _goal_chunks(first: str) -> list[str]:
    chunks: list[str] = []
    if FIRST_GOALS in first:
        after = first.split(FIRST_GOALS, 1)[1]
        cut = re.split(r"\n\s*About |\n\*\*Uses:", after, maxsplit=1)[0]
        for line in cut.splitlines():
            line = line.strip()
            if line.startswith(("-", "*")):
                chunks.append(re.sub(r"^[-*]\s*", "", line))
            elif line:
                chunks.extend(part.strip() for part in line.split(";") if part.strip())
    if "You will be able to:" in first:
        after = first.split("You will be able to:", 1)[1]
        cut = re.split(r"\n\s*About |\n\*\*Uses:", after, maxsplit=1)[0]
        for part in re.split(r"[;.]", cut):
            part = part.strip().lstrip("*").strip()
            if part:
                chunks.append(part)
    return [chunk.lstrip(":").strip() for chunk in chunks if chunk.strip()]


@pytest.mark.parametrize("path", LESSONS, ids=lambda path: path.relative_to(ROOT).as_posix())
def test_lesson_has_the_depth_sections(path: pathlib.Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook["cells"]
    first = _text(cells[0]) if cells else ""
    tier = TIER.search(first)
    assert tier, "first cell needs **Tier:** Core, Intermediate, or Deep"
    sections = dict(_sections(cells))
    why = sections.get("Why it works this way", "")
    minimum = 120 if tier.group(1) == "Core" else 250
    assert len(WORD.findall(why)) >= minimum, (
        f"Why it works this way has {len(WORD.findall(why))} words; need {minimum}"
    )
    assert "When to use it" in sections, "missing ## When to use it"
    uses = USES.search(first)
    assert uses and ("](" in uses.group(0) or "nothing yet" in uses.group(0)), (
        "**Uses:** must be a link or 'nothing yet'"
    )
    whole = "\n".join(_text(cell) for cell in cells)
    assert normalize("not the practice problem") not in normalize(whole)
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown" or not MISTAKE.search(_text(cell)):
            continue
        for follower in cells[index + 1 :]:
            if follower.get("cell_type") != "code":
                follower_text = _text(follower).lstrip()
                if follower.get("cell_type") == "markdown" and follower_text.startswith("## "):
                    break
                continue
            tags = follower.get("metadata", {}).get("tags", [])
            lines = [line for line in _text(follower).splitlines() if line.strip()]
            assert len(lines) >= 3 or "real-mistake-short" in tags, (
                "common-mistake code is shorter than 3 lines"
            )
            break


@pytest.mark.parametrize("path", LESSONS, ids=lambda path: path.relative_to(ROOT).as_posix())
def test_lesson_has_the_flow_sections(path: pathlib.Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook["cells"]
    first = _text(cells[0]) if cells else ""
    whole = "\n".join(_text(cell) for cell in cells)
    headings = _headings(cells)
    rel = path.relative_to(ROOT).as_posix()

    assert FIRST_WHY in first, "first cell needs **Why you'd use this:**"
    assert FIRST_GOALS in first, "first cell needs **After this lesson you can:**"
    for goal in _goal_chunks(first):
        assert not normalize(goal).startswith("predict"), (
            f'goal must not start with "predict": {goal}'
        )
    assert not any(normalize(heading).startswith("predict") for heading in headings), (
        "## Predict heading must not remain"
    )
    assert not PREDICT_HEADING.search(whole), "## Predict heading must not remain"
    if normalize("predict cell") in normalize(whole):
        if rel in pending("G12"):
            pytest.xfail("listed under G12 in docs/maintainers/status.md")
        pytest.fail('learner markdown must not contain "predict cell"')
    elif rel in pending("G12"):
        pytest.fail(f"{rel} is listed under G12 but no longer contains predict cell; remove it")

    if rel.startswith("patterns/"):
        assert "Quick review" in headings, "pattern lesson needs ## Quick review"
        return

    required = [
        heading
        for heading in COURSE_FLOW
        if not (rel == FIRST_COURSE_LESSON and heading == "Quick review")
    ]
    positions: list[int] = []
    for heading in required:
        assert heading in headings, f"missing ## {heading}"
        positions.append(headings.index(heading))
    assert positions == sorted(positions), "flow headings are out of order"
