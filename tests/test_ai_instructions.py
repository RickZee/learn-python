"""Every AI tool gets the same tutor instructions, word for word."""

from __future__ import annotations

import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "docs" / "guides" / "ai-prompts" / "tutor-prompt.md"
WRAPPERS = (
    ".cursor/rules/practice-tutor.mdc",
    ".claude/output-styles/python-tutor.md",
    "docs/guides/ai-prompts/claude-project-instructions.md",
)


@pytest.mark.parametrize("wrapper", WRAPPERS)
def test_wrapper_contains_canonical_tutor_text(wrapper: str) -> None:
    canonical = CANONICAL.read_text(encoding="utf-8").strip()
    text = (ROOT / wrapper).read_text(encoding="utf-8")
    assert canonical in text, f"{wrapper} drifted from docs/guides/ai-prompts/tutor-prompt.md"


def test_learner_profile() -> None:
    settings = json.loads((ROOT / ".claude" / "learner-settings.json").read_text(encoding="utf-8"))
    assert settings["outputStyle"] == "Python tutor"
    deny = settings["permissions"]["deny"]
    assert "Read(**/solutions/**)" in deny
    assert "Edit(**/*-practice.ipynb)" in deny
