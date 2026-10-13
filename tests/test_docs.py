"""Learner-facing Markdown stays reachable, navigable, and short."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    "review",
    ".venv",
    ".pytest_cache",
    ".archive",
    ".claude",
    ".cursor",
    ".git",
    "node_modules",
}
SKIP_FILES = {"AGENTS.md", "CLAUDE.md"}
SKIP_PREFIXES = (
    "docs/guides/ai-prompts/",
    "docs/ai/",  # moves to guides/ai-prompts in D3; skip prompts either way
)
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
WORD = re.compile(r"[A-Za-z0-9']+")
COMMAND_LINE = re.compile(r"^(uv |git |claude |pip )")
BANNED = (
    ("practise", re.compile(r"\bpractise\b")),
    ("Pass 1", re.compile(r"\bPass 1\b")),
    ("Replace `...`", re.compile(r"Replace `\.\.\.`")),
    ("use case", re.compile(r"\buse cases?\b", re.IGNORECASE)),
    ("track", re.compile(r"\b[Tt]racks?\b")),
)


def _md_files() -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        parts = pathlib.PurePosixPath(rel).parts
        if parts and parts[0] in SKIP_DIRS:
            continue
        if any(part in SKIP_DIRS for part in parts):
            continue
        if rel in SKIP_FILES:
            continue
        if any(rel.startswith(prefix) for prefix in SKIP_PREFIXES):
            continue
        # Answer-key walkthroughs are not part of the learner nav graph.
        if rel.startswith("solutions/") and rel != "solutions/README.md":
            continue
        found.append(path)
    return sorted(found)


def _text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_fences(text: str) -> tuple[str, list[str]]:
    """Return (text with fences removed, list of fenced bodies)."""
    bodies: list[str] = []
    out: list[str] = []
    in_fence = False
    buf: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_fence:
                bodies.append("\n".join(buf))
                buf = []
                in_fence = False
            else:
                in_fence = True
            continue
        if in_fence:
            buf.append(line)
        else:
            out.append(line)
    return "\n".join(out), bodies


def _resolve(link: str, from_path: pathlib.Path) -> pathlib.Path | None:
    target = link.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.endswith("/"):
        target = target.rstrip("/") + "/README.md"
    path = (from_path.parent / target).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        return None
    if path.is_dir():
        readme = path / "README.md"
        return readme if readme.exists() else None
    return path if path.exists() else None


def _reachable() -> set[pathlib.Path]:
    start = ROOT / "README.md"
    seen: set[pathlib.Path] = set()
    stack = [start]
    while stack:
        path = stack.pop()
        if path in seen or not path.exists():
            continue
        seen.add(path)
        if path.suffix != ".md":
            continue
        for _, href in LINK.findall(_text(path)):
            dest = _resolve(href, path)
            if dest is not None and dest.suffix == ".md":
                stack.append(dest)
    return seen


def _word_limit(path: pathlib.Path) -> int:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("docs/reference/") or rel.startswith("docs/teaching/"):
        return 1000
    if rel == "docs/guides/learning-with-ai.md":
        return 1000
    if rel == "docs/maintainers/authoring.md":
        return 10_000  # agent rules (moved from AGENTS.md); not learner prose
    if rel == "docs/maintainers/status.md":
        return 10_000  # pending path list for guards; not learner prose
    if rel == "challenges/python-questions.md":
        return 10_000
    if rel == "challenges/README.md":
        return 2_000  # 68-problem index table; not essay prose
    return 600


def _needs_nav(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in {"README.md", "docs/README.md"}:
        return False
    if rel.startswith("docs/reference/"):
        return False
    return bool(rel.startswith("docs/") or path.name == "README.md")


def test_docs_are_reachable_navigable_and_short() -> None:
    files = _md_files()
    reachable = _reachable()
    orphans = [
        path
        for path in files
        if path.resolve() not in {p.resolve() for p in reachable} and path != ROOT / "README.md"
    ]
    assert not orphans, "orphan docs:\n" + "\n".join(
        p.relative_to(ROOT).as_posix() for p in orphans
    )

    problems: list[str] = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = _text(path)
        prose, _ = _strip_fences(text)
        words = len(WORD.findall(prose))
        limit = _word_limit(path)
        if words > limit:
            problems.append(f"{rel}: {words} words > {limit}")

        if _needs_nav(path):
            if "›" not in text and " > " not in text.splitlines()[0:5].__repr__():
                # breadcrumb uses › per writing rules
                head = "\n".join(text.splitlines()[:8])
                if "›" not in head and not re.search(r"\[Home\]", head):
                    problems.append(f"{rel}: missing breadcrumb")
            if "**Next:**" not in text and "**Next**:" not in text:
                problems.append(f"{rel}: missing **Next:**")

        for label, pattern in BANNED:
            # "track" as a noun for a section — flag heading/table uses of Track
            if label == "track":
                if re.search(r"^## Tracks\b", text, re.MULTILINE) or re.search(
                    r"\|\s*Track\s*\|", text
                ):
                    problems.append(f"{rel}: banned '{label}'")
                continue
            if (
                label == "use case"
                and "use-cases" in text
                and not pattern.search(text.replace("use-cases", ""))
            ):
                continue
            if pattern.search(text):
                # allow folder name use-cases
                if label == "use case":
                    cleaned = re.sub(r"use-cases", "", text, flags=re.IGNORECASE)
                    if not pattern.search(cleaned):
                        continue
                problems.append(f"{rel}: banned '{label}'")

        for line in prose.splitlines():
            stripped = line.strip()
            if COMMAND_LINE.match(stripped):
                problems.append(f"{rel}: command outside fence: {stripped}")

    assert not problems, "doc issues:\n" + "\n".join(problems)
