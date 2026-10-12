"""Relative links in Markdown files and notebook Markdown cells must resolve."""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP = {".venv", ".ipynb_checkpoints", "review", ".git"}


def documents():
    for path in sorted([*ROOT.rglob("*.md"), *ROOT.rglob("*.ipynb")]):
        if SKIP & set(path.relative_to(ROOT).parts):
            continue
        if path.suffix == ".md":
            yield path, path.read_text(encoding="utf-8")
        else:
            cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
            for cell in cells:
                if cell["cell_type"] == "markdown":
                    yield path, "".join(cell["source"])


LESSONS = (
    "course/*/*-lesson.ipynb",
    "patterns/*/*-lesson.ipynb",
    "internals/*/*-lesson.ipynb",
)
USES_LINE = re.compile(r"\*\*Uses:\*\*[^\n]*")


def lesson_notebooks():
    return sorted(path for pattern in LESSONS for path in ROOT.glob(pattern))


def test_uses_lines_are_links() -> None:
    """Every lesson's Uses line is a Markdown link, or says nothing yet."""
    problems = []
    for path in lesson_notebooks():
        cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
        first = "".join(cells[0]["source"]) if cells else ""
        match = USES_LINE.search(first)
        rel = path.relative_to(ROOT)
        if match is None:
            problems.append(f"{rel} has no Uses line in the first cell")
            continue
        line = match.group(0)
        if "](" not in line and "nothing yet" not in line:
            problems.append(f"{rel} Uses line is not a link: {line}")
    assert not problems, "Uses lines:\n" + "\n".join(problems)


def test_relative_links_resolve() -> None:
    broken = []
    for path, text in documents():
        for href in LINK.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (path.parent / href.split("#")[0]).resolve()
            if not target.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {href}")
    assert not broken, "broken links:\n" + "\n".join(broken)
