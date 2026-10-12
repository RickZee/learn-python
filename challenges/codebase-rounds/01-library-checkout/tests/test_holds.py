from library.holds import HoldQueue


def test_holds_are_first_come_first_served():
    queue = HoldQueue()
    queue.join("ada")
    queue.join("grace")
    assert queue.next() == "ada"
    assert queue.next() == "grace"
