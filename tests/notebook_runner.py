"""Shared notebook execution helpers with retries for CI flakes."""

from __future__ import annotations

import pathlib
import time

import nbformat
from nbclient import NotebookClient

# Kernel TCP port races under xdist show up as these.
_RETRY_MARKERS = (
    "Address already in use",
    "Kernel died before replying",
    "Kernel didn't respond",
    "ZMQError",
)


def execute_notebook(
    nb: nbformat.NotebookNode,
    path: pathlib.Path,
    *,
    allow_errors: bool = False,
    attempts: int = 3,
) -> NotebookClient:
    last: BaseException | None = None
    for attempt in range(attempts):
        # Fresh copy so a failed start cannot leave half-executed cells behind.
        working = nbformat.from_dict(nb)
        client = NotebookClient(
            working,
            timeout=120,
            startup_timeout=30,
            kernel_name="python3",
            allow_errors=allow_errors,
            record_timing=False,
            resources={"metadata": {"path": str(path.parent)}},
        )
        try:
            client.execute()
        except BaseException as exc:  # noqa: BLE001 - retry then re-raise
            last = exc
            message = f"{type(exc).__name__}: {exc}"
            if attempt + 1 >= attempts or not any(marker in message for marker in _RETRY_MARKERS):
                raise
            time.sleep(0.5 * (attempt + 1))
            continue
        nb.cells = working.cells
        nb.metadata = working.metadata
        return client
    assert last is not None
    raise last
