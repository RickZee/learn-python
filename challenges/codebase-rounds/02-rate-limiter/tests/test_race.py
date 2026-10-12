import threading

from limiter.limiter import Limiter


def test_allow_is_thread_safe():
    limiter = Limiter(limit=10_000)
    threads = [
        threading.Thread(target=lambda: [limiter.allow("a") for _ in range(50)])
        for _ in range(4)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert limiter.total == 200, f"lost updates: total={limiter.total}"
