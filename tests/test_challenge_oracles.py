"""Every challenge oracle is slow, correct, and distinct from the reference."""

from __future__ import annotations

import ast
import importlib.util
import pathlib
import time

import pytest

from pylearn.challenges import ORACLES, cross_check
from pylearn.challenges.oracles import slow_edit_distance
from tests.test_no_leaks import _normalize_body

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOLUTIONS = ROOT / "solutions" / "challenges" / "problems"
PROBLEMS = ROOT / "challenges" / "problems"


def _load_solution(slug: str):
    path = SOLUTIONS / f"{slug}.py"
    spec = importlib.util.spec_from_file_location(f"sol_{slug}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_registered_slug_has_a_notebook() -> None:
    from pylearn.challenges import oracles  # noqa: F401

    for slug in ORACLES:
        path = PROBLEMS / f"{slug}.ipynb"
        assert path.is_file(), f"missing notebook for oracle {slug}"


def test_edit_distance_oracle_agrees_with_reference() -> None:
    from pylearn.challenges import oracles  # noqa: F401

    sol = _load_solution("57-edit-distance").min_distance
    cross_check("57-edit-distance", sol, trials=40, seed=0)


def test_edit_distance_oracle_ast_differs_from_reference() -> None:
    sol_src = (SOLUTIONS / "57-edit-distance.py").read_text(encoding="utf-8")
    sol_tree = ast.parse(sol_src)
    sol_fn = next(
        n for n in sol_tree.body if isinstance(n, ast.FunctionDef) and n.name == "min_distance"
    )
    oracle_src = (ROOT / "src/pylearn/challenges/oracles.py").read_text(encoding="utf-8")
    oracle_tree = ast.parse(oracle_src)
    oracle_fn = next(
        n
        for n in oracle_tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "slow_edit_distance"
    )
    assert _normalize_body(oracle_fn) != _normalize_body(sol_fn)


def test_edit_distance_oracle_is_fast_enough_on_its_cases() -> None:
    from pylearn.challenges import oracles  # noqa: F401

    oracle = ORACLES["57-edit-distance"]
    import random

    rng = random.Random(0)
    cases = oracle.cases(rng)
    start = time.perf_counter()
    for _ in range(40):
        args = next(cases)
        oracle.slow(*args)
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"oracle took {elapsed:.2f}s on its cases"


def test_wrong_edit_distance_variant_is_caught() -> None:
    """A classic bug: never replace, only insert/delete."""

    def wrong(a: str, b: str) -> int:
        if not a or not b:
            return len(a) + len(b)
        if a[0] == b[0]:
            return wrong(a[1:], b[1:])
        return 1 + min(wrong(a[1:], b), wrong(a, b[1:]))  # no replace

    with pytest.raises(AssertionError, match="slow correct version"):
        cross_check("57-edit-distance", wrong, trials=40, seed=0)


def test_slow_edit_distance_known_cases() -> None:
    assert slow_edit_distance("horse", "ros") == 3
    assert slow_edit_distance("", "abc") == 3
    assert slow_edit_distance("same", "same") == 0
