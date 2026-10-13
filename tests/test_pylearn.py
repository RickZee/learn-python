"""Unit tests for pylearn.check and pylearn.challenges.cross_check."""

from __future__ import annotations

import pytest

from pylearn.challenges import cross_check
from pylearn.challenges.oracles import slow_edit_distance
from pylearn.check import NOT_WRITTEN, check


def test_check_match_prints() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    check(add, 2, 3, expect=5)


def test_check_mismatch_message() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    with pytest.raises(AssertionError, match=r"add\(2, 3\) returned 5; expected 9"):
        check(add, 2, 3, expect=9)


def test_check_tol() -> None:
    def almost() -> float:
        return 0.1 + 0.2

    check(almost, expect=0.3, tol=1e-9)


def test_check_not_implemented_message() -> None:
    def stub() -> int:
        raise NotImplementedError

    with pytest.raises(AssertionError, match=NOT_WRITTEN):
        check(stub, expect=1)


def test_cross_check_agreement() -> None:
    cross_check("57-edit-distance", slow_edit_distance, trials=20, seed=1)


def test_cross_check_counterexample_message() -> None:
    def wrong(a: str, b: str) -> int:
        return abs(len(a) - len(b))  # ignores substitutions

    with pytest.raises(AssertionError, match="slow correct version"):
        cross_check("57-edit-distance", wrong, trials=40, seed=0)


def test_cross_check_not_written_message() -> None:
    def stub(a: str, b: str) -> int:
        raise NotImplementedError

    with pytest.raises(AssertionError, match=NOT_WRITTEN):
        cross_check("57-edit-distance", stub, trials=1, seed=0)
