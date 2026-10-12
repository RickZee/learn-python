def sum_stack(nums: list[int]) -> int:
    pending = list(nums)
    total = 0
    while pending:
        total += pending.pop()
    return total


def flatten(items: list) -> list:
    pending = [items]
    flat = []
    while pending:
        current = pending.pop()
        if isinstance(current, list):
            for item in reversed(current):
                pending.append(item)
        else:
            flat.append(current)
    return flat


def depth_stack(items: list) -> int:
    pending = [(items, 1)]
    best = 0
    while pending:
        current, depth = pending.pop()
        if not isinstance(current, list):
            continue
        best = max(best, depth)
        for item in current:
            pending.append((item, depth + 1))
    return best
