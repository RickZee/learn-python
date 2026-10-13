from triage.classify import classify_all_bounded


class Counting:
    def __init__(self) -> None:
        self.calls = 0

    def classify(self, text: str) -> str:
        self.calls += 1
        return "other"


def test_bounded_preserves_order():
    tickets = classify_all_bounded(Counting(), ["a", "b", "c"], workers=2)
    assert [t.text for t in tickets] == ["a", "b", "c"]


def test_bounded_calls_each_once():
    client = Counting()
    classify_all_bounded(client, ["a", "b"], workers=2)
    assert client.calls == 2
