from collections import deque


def pop_front(items: list[int]) -> int:
    queue = deque(items)
    value = queue.popleft()
    return value


def rotate_queue(items: list[int], k: int) -> list[int]:
    queue = deque(items)
    for _ in range(k):
        if not queue:
            break
        queue.append(queue.popleft())
    return list(queue)


def tail(items: list[int], k: int) -> list[int]:
    return list(deque(items, maxlen=k))
