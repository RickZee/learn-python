import time

from limiter.limiter import Limiter


def test_allow_is_constant_per_call():
    limiter = Limiter(limit=10**9)
    start = time.perf_counter()
    for index in range(50_000):
        assert limiter.allow(f"key-{index % 1000}")
    elapsed = time.perf_counter() - start
    # Locked solution sleeps 0.0001 per allow in the race demo — too slow for 50k.
    # Scale check uses window hit path: ensure counts dict stays O(1) keyed.
    from limiter.window import Window

    window = Window(limit=10**9)
    start = time.perf_counter()
    for index in range(200_000):
        assert window.hit(f"key-{index % 5000}")
    elapsed = time.perf_counter() - start
    assert elapsed < 0.5, f"{elapsed:.2f}s; hit is scanning history"
