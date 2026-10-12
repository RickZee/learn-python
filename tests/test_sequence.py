"""Course notebooks may use a concept only after the lesson that introduces it."""

from tools.check_sequence import violations


def test_concepts_follow_the_ledger() -> None:
    found = violations()
    assert not found, "concept used before its lesson:\n" + "\n".join(found)


def test_loops_are_introduced_before_lists() -> None:
    from tools.check_sequence import introduced

    assert introduced()["loops"] < "course/04-collections/01-lists-lesson.ipynb"
