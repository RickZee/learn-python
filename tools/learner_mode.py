"""Opt-in Cursor learner mode: block solutions/ and force the tutor rule."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CURSORIGNORE = """.cursorignore written by tools/learner_mode.py — do not commit.
solutions/
docs/maintainers/review/
"""

RULE_BODY = """---
description: Learner mode (written by tools/learner_mode.py). Do not commit.
alwaysApply: true
---

The user is a learner. Apply practice-tutor.mdc to every message.
Do not read files under solutions/.
"""


def _paths(root: Path) -> tuple[Path, Path]:
    return root / ".cursorignore", root / ".cursor" / "rules" / "learner-mode.mdc"


def cmd_on(root: Path) -> None:
    ignore, rule = _paths(root)
    rule.parent.mkdir(parents=True, exist_ok=True)
    ignore.write_text(CURSORIGNORE, encoding="utf-8")
    rule.write_text(RULE_BODY, encoding="utf-8")
    print(f"learner mode on ({ignore}, {rule})")


def cmd_off(root: Path) -> None:
    ignore, rule = _paths(root)
    removed = []
    for path in (ignore, rule):
        if path.exists():
            path.unlink()
            removed.append(str(path))
    if removed:
        print("learner mode off; removed " + ", ".join(removed))
    else:
        print("learner mode already off")


def cmd_status(root: Path) -> None:
    ignore, rule = _paths(root)
    if ignore.exists() and rule.exists():
        print("learner mode: on")
    elif ignore.exists() or rule.exists():
        print("learner mode: partial (run on or off to repair)")
    else:
        print("learner mode: off")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("on", "off", "status"))
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repo root (default: cwd); tests pass a temp dir",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "on":
        cmd_on(root)
    elif args.command == "off":
        cmd_off(root)
    else:
        cmd_status(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
