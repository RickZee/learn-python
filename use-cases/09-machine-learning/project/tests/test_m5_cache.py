from pathlib import Path

from triage.classify import classify_cached


class Counting:
    def __init__(self) -> None:
        self.calls = 0

    def classify(self, text: str) -> str:
        self.calls += 1
        return "billing"


def test_cache_hits(tmp_path: Path):
    client = Counting()
    first = classify_cached(client, ["lost card"], tmp_path)
    second = classify_cached(client, ["lost card"], tmp_path)
    assert first[0].label == "billing"
    assert second[0].label == "billing"
    assert client.calls == 1


def test_cache_writes_file(tmp_path: Path):
    classify_cached(Counting(), ["lost card"], tmp_path)
    assert any(tmp_path.iterdir())
