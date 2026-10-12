from triage.classify import accuracy, classify_all


class FakeClient:
    def __init__(self) -> None:
        self.calls = 0

    def classify(self, text: str) -> str:
        self.calls += 1
        if self.calls == 1:
            raise TimeoutError("slow")
        if "card" in text:
            return "billing"
        return "other"


def test_retries_then_labels():
    tickets = classify_all(FakeClient(), ["lost card", "hello"])
    assert [ticket.label for ticket in tickets] == ["billing", "other"]


def test_accuracy():
    tickets = classify_all(FakeClient(), ["lost card", "hello"])
    assert accuracy(tickets, ["billing", "other"]) == 1.0
