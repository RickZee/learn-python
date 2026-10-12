"""Your checks must fail on the buggy module and pass on the good one."""

import sys
from pathlib import Path

from pylearn import load_exercise

sys.path.insert(0, str(Path(__file__).parent))
import buggy  # noqa: E402
import good  # noqa: E402

checks = load_exercise("checks")


def _rejects(check, func) -> bool:
    try:
        check(func)
    except Exception:
        return True
    return False


def test_word_count_check_catches_the_bug():
    assert _rejects(checks.check_word_count, buggy.word_count)
    checks.check_word_count(good.word_count)


def test_shout_check_catches_the_bug():
    assert _rejects(checks.check_shout, buggy.shout)
    checks.check_shout(good.shout)


def test_first_word_check_catches_the_bug():
    assert _rejects(checks.check_first_word, buggy.first_word)
    checks.check_first_word(good.first_word)
