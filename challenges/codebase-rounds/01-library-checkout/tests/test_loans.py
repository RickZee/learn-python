from library.loans import checkout


def test_patrons_do_not_share_loans():
    first = checkout("ada", "dune")
    second = checkout("grace", "emma")
    assert first == [("ada", "dune")]
    assert second == [("grace", "emma")]
