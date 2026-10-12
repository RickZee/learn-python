"""Re-run lesson notebooks in place and clear outputs from practice notebooks.

Usage:
    uv run python tools/refresh_outputs.py            # every notebook
    uv run python tools/refresh_outputs.py PATH ...   # just these
"""

from __future__ import annotations

import pathlib
import sys

import nbformat
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP = {".venv", ".ipynb_checkpoints", "solutions", "review"}


def is_practice(path: pathlib.Path) -> bool:
    return path.name.endswith("-practice.ipynb") or "problems" in path.parts


def notebooks(args: list[str]) -> list[pathlib.Path]:
    if args:
        return [pathlib.Path(arg).resolve() for arg in args]
    found = ROOT.rglob("*.ipynb")
    return sorted(p for p in found if not SKIP & set(p.relative_to(ROOT).parts))


def tidy_metadata(nb: nbformat.NotebookNode) -> None:
    """Drop kernel bookkeeping that is not part of the lesson.

    The kernel reports its version and per-cell timings. The version belongs in
    .python-version, and the timings change on every run.
    """
    info = nb.metadata.get("language_info")
    if info is not None:
        nb.metadata["language_info"] = {
            "name": info.get("name", "python"),
            "pygments_lexer": info.get("pygments_lexer", "ipython3"),
        }
    for cell in nb.cells:
        if "execution" in cell.get("metadata", {}):
            del cell.metadata["execution"]


def main(args: list[str]) -> None:
    for path in notebooks(args):
        nb = nbformat.read(path, as_version=4)
        if is_practice(path):
            for cell in nb.cells:
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None
        else:
            NotebookClient(
                nb,
                timeout=60,
                kernel_name="python3",
                record_timing=False,
                resources={"metadata": {"path": str(path.parent)}},
            ).execute()
        tidy_metadata(nb)
        nbformat.write(nb, path)
        print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
