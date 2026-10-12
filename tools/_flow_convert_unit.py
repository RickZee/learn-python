"""Convert old Predict-first lessons to the teach-first flow in AGENTS.md.

Usage:
  uv run python tools/_flow_convert_unit.py course/00-start \\
      --first course/00-start/01-first-program-lesson.ipynb=FIRST.json \\
      ...

Or pass a JSON map file:
  uv run python tools/_flow_convert_unit.py --map path/to/map.json

The map is { "relative/path.ipynb": { "first": "...", "quick_review": "..."|null } }.
quick_review null means omit (only for the first course lesson).
Empty string means auto-generate a minimal quick review from Uses links.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
STOP = object()


def _text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def _set_source(cell: dict, src: str) -> dict:
    if src and not src.endswith("\n"):
        src += "\n"
    cell = dict(cell)
    cell["source"] = [src]
    return cell


def _md(src: str) -> dict:
    if src and not src.endswith("\n"):
        src += "\n"
    return {"cell_type": "markdown", "metadata": {}, "source": [src]}


def _split_sections(cells: list[dict]) -> tuple[dict, list[tuple[str, list[dict]]]]:
    first = cells[0]
    sections: list[tuple[str, list[dict]]] = []
    current: str | None = None
    buf: list[dict] = []
    for cell in cells[1:]:
        if cell.get("cell_type") == "markdown":
            line = _text(cell).lstrip().splitlines()[0] if _text(cell).strip() else ""
            if line.startswith("## "):
                if current is not None:
                    sections.append((current, buf))
                current = line[3:].strip()
                buf = [cell]
                continue
        if current is None:
            # preamble after first cell without a heading — attach to a synthetic block
            sections.append(("", [cell]))
            continue
        buf.append(cell)
    if current is not None:
        sections.append((current, buf))
    return first, sections


def _rename_predict_block(cells: list[dict]) -> list[dict]:
    out: list[dict] = []
    for cell in cells:
        src = _text(cell)
        if cell.get("cell_type") == "markdown":
            src = src.replace("## Predict", "## Check yourself", 1)
            src = src.replace(
                "Write down what each line prints before you run it.",
                "Answer these from the example above before you run the cell.",
            )
            src = src.replace(
                "Answer from the idea above before you run the cell.",
                "Answer these from the example above before you run the cell.",
            )
            src = src.replace("Check your predictions", "Check your answers")
            out.append(_set_source(cell, src))
        else:
            out.append(cell)
    return out


def _rename_modify(cells: list[dict]) -> list[dict]:
    out: list[dict] = []
    for cell in cells:
        src = _text(cell)
        if cell.get("cell_type") == "markdown" and src.lstrip().startswith("## Modify"):
            src = src.replace("## Modify", "## Try it", 1)
            out.append(_set_source(cell, src))
        else:
            out.append(cell)
    return out


def _rename_worked(cells: list[dict]) -> list[dict]:
    out: list[dict] = []
    for cell in cells:
        src = _text(cell)
        if cell.get("cell_type") == "markdown" and src.lstrip().startswith(
            "## Worked example"
        ):
            src = src.replace("## Worked example", "## See it work", 1)
            out.append(_set_source(cell, src))
        else:
            out.append(cell)
    return out


def _merge_investigate_into_check(
    check_cells: list[dict], investigate_cells: list[dict]
) -> list[dict]:
    if not investigate_cells:
        return check_cells
    # Drop the ## Investigate heading; keep body questions before the check answers if any.
    body = []
    for cell in investigate_cells:
        src = _text(cell)
        if cell.get("cell_type") == "markdown" and src.lstrip().startswith(
            "## Investigate"
        ):
            rest = re.sub(r"^##\s+Investigate\s*\n?", "", src.lstrip())
            if rest.strip():
                body.append(_md(rest))
            continue
        body.append(cell)
    # Insert investigate body after the Check yourself heading cell, before code.
    if not check_cells:
        return [_md("## Check yourself")] + body
    return [check_cells[0]] + body + check_cells[1:]


def _default_quick_review(first: str) -> str:
    uses = re.search(r"\*\*Uses:\*\*\s*(.+)", first)
    topic = "what you just learned"
    if uses and "nothing yet" not in uses.group(1):
        topic = uses.group(1).strip().rstrip(".")
    return (
        "## Quick review\n\n"
        f"1. In one sentence, what did you take from {topic}?\n"
        "2. What is one mistake you already know to watch for?\n\n"
        "<details><summary>Answers</summary>\n\n"
        "Your own words are fine. Skim the linked lesson if a question feels blank.\n"
        "</details>"
    )


def convert_notebook(path: pathlib.Path, first: str, quick_review: str | None) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    _, sections = _split_sections(nb["cells"])
    by_name = {name: cells for name, cells in sections if name}

    if quick_review == "":
        quick_review = _default_quick_review(first)

    # Already converted?
    if "See it work" in by_name and "Check yourself" in by_name:
        cells = nb["cells"]
        cells[0] = _set_source(cells[0], first)
        if quick_review is not None:
            if not (
                len(cells) > 1
                and _text(cells[1]).lstrip().startswith("## Quick review")
            ):
                cells.insert(1, _md(quick_review))
            else:
                cells[1] = _set_source(cells[1], quick_review)
        nb["cells"] = cells
        path.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return

    idea = by_name.get("The idea", [])
    predict = _rename_predict_block(by_name.get("Predict", []))
    worked = _rename_worked(by_name.get("Worked example", []))
    why = by_name.get("Why it works this way", [])
    when = by_name.get("When to use it", [])
    mistake = by_name.get("Common mistake", [])
    investigate = by_name.get("Investigate", [])
    modify = _rename_modify(by_name.get("Modify", []))
    recap = by_name.get("Recap", [])

    # Keep any other named sections (e.g. ## input) after See it work.
    known = {
        "The idea",
        "Predict",
        "Worked example",
        "Why it works this way",
        "When to use it",
        "Common mistake",
        "Investigate",
        "Modify",
        "Recap",
        "Quick review",
        "See it work",
        "Check yourself",
        "Try it",
    }
    extras: list[dict] = []
    for name, cells in sections:
        if name and name not in known:
            extras.extend(cells)

    check = _merge_investigate_into_check(predict, investigate)
    if check and _text(check[0]).lstrip().startswith("## Check yourself"):
        pass
    elif predict:
        check = predict
    else:
        check = [_md("## Check yourself\n\n(What does the example print?)")]

    new_cells: list[dict] = [_set_source(nb["cells"][0], first)]
    if quick_review is not None:
        new_cells.append(_md(quick_review))
    new_cells.extend(idea)
    new_cells.extend(worked)
    new_cells.extend(check)
    new_cells.extend(why)
    new_cells.extend(when)
    new_cells.extend(mistake)
    new_cells.extend(modify)
    new_cells.extend(extras)
    new_cells.extend(recap)

    nb["cells"] = new_cells
    path.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=pathlib.Path, required=True)
    args = parser.parse_args()
    mapping = json.loads(args.map.read_text(encoding="utf-8"))
    for rel, spec in mapping.items():
        path = ROOT / rel
        if not path.exists():
            print(f"missing {rel}", file=sys.stderr)
            return 1
        convert_notebook(path, spec["first"], spec.get("quick_review", ""))
        print("converted", rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
