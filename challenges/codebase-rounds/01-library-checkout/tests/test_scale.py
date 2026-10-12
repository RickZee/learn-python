import time

from library.store import Store


def test_find_uses_an_index():
    titles = [f"book-{index}" for index in range(100_000)]
    store = Store(titles)
    target = "book-99999"
    start = time.perf_counter()
    for _ in range(500):
        assert store.find(target) == 99_999
    elapsed = time.perf_counter() - start
    assert elapsed < 0.05, f"{elapsed:.2f}s; find is still a linear scan"
