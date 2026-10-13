"""Every AI tool gets the same tutor instructions, word for word."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

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


def test_g15_agents_names_authoring() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/maintainers/authoring.md" in text


def test_g15_learner_mode_on_off(tmp_path: pathlib.Path) -> None:
    script = ROOT / "tools" / "learner_mode.py"
    on = subprocess.run(
        [sys.executable, str(script), "on", "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert on.returncode == 0
    ignore = tmp_path / ".cursorignore"
    rule = tmp_path / ".cursor" / "rules" / "learner-mode.mdc"
    assert ignore.is_file()
    assert "solutions/" in ignore.read_text(encoding="utf-8")
    assert rule.is_file()
    rule_text = rule.read_text(encoding="utf-8")
    assert "alwaysApply: true" in rule_text

    off = subprocess.run(
        [sys.executable, str(script), "off", "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert off.returncode == 0
    assert not ignore.exists()
    assert not rule.exists()


def test_g15_gitignore_lists_learner_mode_paths() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".cursorignore" in text
    assert ".cursor/rules/learner-mode.mdc" in text
