from triage.classify import accuracy, classify_all


class FakeClient:
    def classify(self, text: str) -> str:
        return "billing" if "card" in text else "other"


def test_classify_all():
    tickets = classify_all(FakeClient(), ["lost card", "hello"])
    assert [t.label for t in tickets] == ["billing", "other"]


def test_accuracy():
    tickets = classify_all(FakeClient(), ["lost card", "hello"])
    assert accuracy(tickets, ["billing", "other"]) == 1.0
