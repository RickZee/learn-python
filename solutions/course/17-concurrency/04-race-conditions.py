import threading
import time


def safe_bump(counter: dict, lock: threading.Lock) -> None:
    with lock:
        counter["value"] += 1


def locked_total(workers: int) -> int:
    counter = {"value": 0}
    lock = threading.Lock()

    def bump() -> None:
        with lock:
            value = counter["value"]
            time.sleep(0.01)
            counter["value"] = value + 1

    threads = [threading.Thread(target=bump) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return counter["value"]


def lost_update() -> bool:
    counter = 0

    def bump() -> None:
        nonlocal counter
        value = counter
        time.sleep(0.01)
        counter = value + 1

    threads = [threading.Thread(target=bump) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return counter == 1


def counter_style() -> str:
    return "with lock"
