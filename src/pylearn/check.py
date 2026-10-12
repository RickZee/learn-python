"""Friendly checks for practice notebooks and exercise tests."""

from __future__ import annotations

import importlib.util
import inspect
import math
import os
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

NOT_WRITTEN = "not written yet. Replace `raise NotImplementedError` with your code."


def check(func: Callable[..., Any], *args: Any, expect: Any, tol: float | None = None) -> None:
    """Call ``func(*args)`` and compare the result with ``expect``.

    Prints one line when it matches. Raises AssertionError that names the call,
    the result, and the expected value when it does not. Pass ``tol`` to compare
    floats with a tolerance.
    """
    call = f"{func.__name__}({', '.join(repr(arg) for arg in args)})"
    try:
        got = func(*args)
    except NotImplementedError:
        raise AssertionError(f"{call} is {NOT_WRITTEN}") from None
    same = math.isclose(got, expect, abs_tol=tol) if tol is not None else got == expect
    if not same:
        raise AssertionError(f"{call} returned {got!r}; expected {expect!r}")
    print(f"✓ {call} == {expect!r}")


def _repo_root(start: Path) -> Path:
    for folder in (start, *start.parents):
        if (folder / "pyproject.toml").exists():
            return folder
    raise FileNotFoundError(f"no pyproject.toml above {start}")


def load_exercise(name: str) -> ModuleType:
    """Load ``<name>.py`` from the folder of the test file that calls this.

    With the environment variable PYLEARN_SOLUTIONS=1 (CI sets it), load the
    reference solution from the same relative path under ``solutions/``.
    """
    folder = Path(inspect.stack()[1].filename).resolve().parent
    if os.environ.get("PYLEARN_SOLUTIONS") == "1":
        root = _repo_root(folder)
        folder = root / "solutions" / folder.relative_to(root)
    path = folder / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"exercise_{name}_{abs(hash(folder))}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
