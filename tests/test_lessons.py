"""Every lesson notebook must run top to bottom in a real kernel, and its saved
output must match what a fresh run prints.

Tag a cell `raises-exception` when the error is the lesson. Tag a cell
`volatile` when its output differs by machine (CPU count, timings, paths).
"""

from __future__ import annotations

import pathlib

import nbformat
import pytest

from tests._status import pending
from tests.notebook_runner import execute_notebook

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "patterns/*/*-lesson.ipynb",
    "internals/*/*-lesson.ipynb",
    "use-cases/*/*.ipynb",
    "challenges/*.ipynb",
)
LESSONS = sorted(path for pattern in PATTERNS for path in ROOT.glob(pattern))


def stdout(cell: nbformat.NotebookNode) -> str:
    return "".join(
        out.get("text", "")
        for out in cell.get("outputs", [])
        if out.get("output_type") == "stream" and out.get("name") == "stdout"
    )


def execute_results(cell: nbformat.NotebookNode) -> list[str]:
    found: list[str] = []
    for out in cell.get("outputs", []):
        if out.get("output_type") != "execute_result":
            continue
        data = out.get("data") or {}
        text = data.get("text/plain", "")
        if isinstance(text, list):
            text = "".join(text)
        found.append(text)
    return found


def error_enames(cell: nbformat.NotebookNode) -> list[str]:
    return [
        out.get("ename", "") for out in cell.get("outputs", []) if out.get("output_type") == "error"
    ]


@pytest.mark.parametrize("path", LESSONS, ids=lambda path: str(path.relative_to(ROOT)))
def test_lesson_runs_and_outputs_are_fresh(path: pathlib.Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    saved = nbformat.read(path, as_version=4)
    fresh = nbformat.read(path, as_version=4)
    execute_notebook(fresh, path)

    for old, new in zip(saved.cells, fresh.cells, strict=True):
        if new.cell_type != "code" or "volatile" in new.metadata.get("tags", []):
            continue
        assert stdout(old) == stdout(new), (
            f"saved stdout is stale in cell {new.get('id')}; "
            "run `uv run python tools/refresh_outputs.py` and commit"
        )
        assert execute_results(old) == execute_results(new), (
            f"saved execute_result is stale in cell {new.get('id')}; "
            "run `uv run python tools/refresh_outputs.py` and commit"
        )
        assert error_enames(old) == error_enames(new), (
            f"saved error ename is stale in cell {new.get('id')}; "
            "run `uv run python tools/refresh_outputs.py` and commit"
        )

    broken_raises = [
        new.get("id")
        for new in fresh.cells
        if new.cell_type == "code"
        and "raises-exception" in new.metadata.get("tags", [])
        and not any(out.get("output_type") == "error" for out in new.get("outputs", []))
    ]
    if broken_raises:
        if rel in pending("G10"):
            pytest.xfail("listed under G10 in docs/maintainers/status.md")
        ids = ", ".join(map(str, broken_raises))
        pytest.fail(f"cells tagged raises-exception have no error output: {ids}")
    elif rel in pending("G10"):
        pytest.fail(f"{rel} is listed under G10 but raises-exception cells now raise; remove it")
