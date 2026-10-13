"""Pattern lessons keep the 9-part body and no padding filler."""

from __future__ import annotations

import json
import pathlib

import pytest

from tests._text import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILLER = "so each step reuses prior work instead of restarting a nested scan"
LESSONS = sorted(ROOT.glob("patterns/*/*-lesson.ipynb"))


def _text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def _headings(cells: list[dict]) -> list[str]:
    found: list[str] = []
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        for line in _text(cell).splitlines():
            if line.startswith("## "):
                found.append(line[3:].strip())
    return found


def _missing_parts(headings: list[str]) -> list[str]:
    checks = {
        "Recognize it": any(h == "Recognize it" for h in headings),
        "Brute force": any("Brute force" in h for h in headings),
        "Key insight": any(h == "Key insight" for h in headings),
        "Worked example": any(h == "Worked example" for h in headings),
        "Trace": any(h.startswith("Trace") for h in headings),
        "Cost": any(h == "Cost" or h.startswith("Cost ") or h == "Complexity" for h in headings),
        "Variants": any(h.startswith("Variants") for h in headings),
        "Common mistake": any("Common mistake" in h for h in headings),
        "Python idioms": any(h == "Python idioms" for h in headings),
    }
    return [name for name, ok in checks.items() if not ok]


@pytest.mark.parametrize("path", LESSONS, ids=lambda path: path.relative_to(ROOT).as_posix())
def test_pattern_lesson_has_substance(path: pathlib.Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    whole = "\n".join(_text(cell) for cell in notebook["cells"])
    normalized = normalize(whole)
    headings = _headings(notebook["cells"])
    problems: list[str] = []
    if normalize("Worked reading") in normalized:
        problems.append("contains Worked reading padding")
    if normalize(FILLER) in normalized:
        problems.append("contains shared Why filler phrase")
    missing = _missing_parts(headings)
    if missing:
        problems.append("missing sections: " + ", ".join(missing))
    assert not problems, "; ".join(problems)
