from triage.classify import classify_all_retry


class Flaky:
    def __init__(self) -> None:
        self.calls = 0

    def classify(self, text: str) -> str:
        self.calls += 1
        if self.calls < 3:
            raise TimeoutError("slow")
        return "billing"


class AlwaysFail:
    def classify(self, text: str) -> str:
        raise TimeoutError("slow")


def test_retry_then_success():
    tickets = classify_all_retry(Flaky(), ["lost card"], failures_allowed=2)
    assert tickets[0].label == "billing"


def test_give_up_unknown():
    tickets = classify_all_retry(AlwaysFail(), ["lost card"], failures_allowed=1)
    assert tickets[0].label == "unknown"
