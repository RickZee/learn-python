"""Projects have milestones with their own tests and Decide prompts (G16)."""

from __future__ import annotations

import pathlib
import re

import pytest

from tests._status import pending

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECTS = sorted(ROOT.glob("use-cases/*/project"))
MILESTONE = re.compile(r"^test_m(\d+)_.*\.py$")
HEADING = re.compile(r"^##\s+(M\d+)\b", re.MULTILINE)


@pytest.mark.parametrize("path", PROJECTS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_g16_project_milestones(path: pathlib.Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if rel in pending("G16"):
        pytest.xfail("listed under G16 in docs/maintainers/status.md")
    tests_dir = path / "tests"
    assert tests_dir.is_dir(), f"missing {rel}/tests"
    milestone_files = sorted(p for p in tests_dir.glob("test_m*_*.py") if MILESTONE.match(p.name))
    assert len(milestone_files) >= 4, (
        f"{rel} has {len(milestone_files)} milestone test files; need ≥ 4"
    )
    readme = path / "README.md"
    assert readme.is_file(), f"missing {rel}/README.md"
    text = readme.read_text(encoding="utf-8")
    headings = HEADING.findall(text)
    for mf in milestone_files:
        number = MILESTONE.match(mf.name).group(1)  # type: ignore[union-attr]
        label = f"M{number}"
        assert label in headings, f"README missing ## {label} for {mf.name}"
        # Decide line in that section
        part = text.split(f"## {label}", 1)[1]
        part = re.split(r"\n## ", part, maxsplit=1)[0]
        assert re.search(r"\*\*Decide\*\*|Decide", part), f"## {label} needs a Decide question"
        source = mf.read_text(encoding="utf-8")
        test_count = len(re.findall(r"^def test_", source, re.MULTILINE))
        assert test_count >= 2, f"{mf.name} has {test_count} tests; need ≥ 2"
