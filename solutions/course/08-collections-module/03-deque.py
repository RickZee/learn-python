from collections import deque


def pop_front(items: list[int]) -> int:
    return deque(items).popleft()


def rotate_queue(items: list[int], k: int) -> list[int]:
    queue = deque(items)
    for _ in range(k):
        if not queue:
            break
        queue.append(queue.popleft())
    return list(queue)


def tail(items: list[int], k: int) -> list[int]:
    recent = deque(maxlen=k)
    for item in items:
        recent.append(item)
    return list(recent)
