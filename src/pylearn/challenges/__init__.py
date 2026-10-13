"""Random cross-checks for challenge problems.

Each problem registers a slow reference that is correct by construction (it tries
every option) and a generator of small random inputs. A learner's function must
agree with the slow reference on every input.
"""

from __future__ import annotations

import copy
import random
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

from pylearn.check import NOT_WRITTEN


@dataclass(frozen=True)
class Oracle:
    slow: Callable[..., Any]
    cases: Callable[[random.Random], Iterator[tuple[Any, ...]]]
    same: Callable[[Any, Any], bool] = lambda got, want: got == want


@dataclass(frozen=True)
class OpsOracle:
    """Slow model class driven by the same random operation sequence as the learner."""

    model: type
    ops: Callable[[random.Random], Iterator[tuple[str, tuple[Any, ...]]]]


ORACLES: dict[str, Oracle] = {}
OPS_ORACLES: dict[str, OpsOracle] = {}


def register(slug: str, oracle: Oracle) -> None:
    ORACLES[slug] = oracle


def register_ops(slug: str, oracle: OpsOracle) -> None:
    OPS_ORACLES[slug] = oracle


def cross_check(slug: str, func: Callable[..., Any], *, trials: int = 40, seed: int = 0) -> None:
    """Compare ``func`` with the slow reference for ``slug`` on random inputs."""
    from pylearn.challenges import oracles  # noqa: F401  (registers every problem)

    oracle = ORACLES[slug]
    rng = random.Random(seed)
    cases = oracle.cases(rng)
    for _ in range(trials):
        args = next(cases)
        want = oracle.slow(*copy.deepcopy(args))
        call = f"{func.__name__}({', '.join(repr(arg) for arg in args)})"
        try:
            got = func(*copy.deepcopy(args))
        except NotImplementedError:
            raise AssertionError(f"{call} is {NOT_WRITTEN}") from None
        if not oracle.same(got, want):
            raise AssertionError(
                f"{call} returned {got!r}; a slow correct version returns {want!r}"
            )
    print(f"✓ {func.__name__} agrees with a slow reference on {trials} random inputs")


def cross_check_ops(slug: str, cls: type, *, trials: int = 40, seed: int = 0) -> None:
    """Drive ``cls`` and a slow model with the same random operations; compare returns."""
    from pylearn.challenges import oracles  # noqa: F401

    oracle = OPS_ORACLES[slug]
    rng = random.Random(seed)
    ops = oracle.ops(rng)
    # First op must construct: ("__init__", args)
    init_name, init_args = next(ops)
    assert init_name == "__init__", f"ops for {slug} must start with __init__"
    try:
        got_obj = cls(*copy.deepcopy(init_args))
    except NotImplementedError:
        raise AssertionError(f"{cls.__name__}(...) is {NOT_WRITTEN}") from None
    want_obj = oracle.model(*copy.deepcopy(init_args))
    compared = 0
    for _ in range(trials):
        name, args = next(ops)
        if name == "__init__":
            try:
                got_obj = cls(*copy.deepcopy(args))
            except NotImplementedError:
                raise AssertionError(f"{cls.__name__}(...) is {NOT_WRITTEN}") from None
            want_obj = oracle.model(*copy.deepcopy(args))
            continue
        call = f"{name}({', '.join(repr(arg) for arg in args)})"
        try:
            got = getattr(got_obj, name)(*copy.deepcopy(args))
        except NotImplementedError:
            raise AssertionError(f"{cls.__name__}.{call} is {NOT_WRITTEN}") from None
        want = getattr(want_obj, name)(*copy.deepcopy(args))
        if got != want:
            raise AssertionError(
                f"{cls.__name__}.{call} returned {got!r}; a slow correct version returns {want!r}"
            )
        compared += 1
    print(f"✓ {cls.__name__} agrees with a slow model on {compared} operations")
