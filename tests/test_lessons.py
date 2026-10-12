"""Every lesson notebook must run top to bottom in a real kernel, and its saved
output must match what a fresh run prints.

Tag a cell `raises-exception` when the error is the lesson. Tag a cell
`volatile` when its output differs by machine (CPU count, timings, paths).
"""

from __future__ import annotations

import pathlib

import nbformat
import pytest

from tests.notebook_runner import execute_notebook

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "course/*/*-skip-test.ipynb",
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


@pytest.mark.parametrize("path", LESSONS, ids=lambda path: str(path.relative_to(ROOT)))
def test_lesson_runs_and_outputs_are_fresh(path: pathlib.Path) -> None:
    saved = nbformat.read(path, as_version=4)
    fresh = nbformat.read(path, as_version=4)
    execute_notebook(fresh, path)
    for old, new in zip(saved.cells, fresh.cells, strict=True):
        if new.cell_type != "code" or "volatile" in new.metadata.get("tags", []):
            continue
        assert stdout(old) == stdout(new), (
            f"saved output is stale in cell {new.get('id')}; "
            "run `uv run python tools/refresh_outputs.py` and commit"
        )
