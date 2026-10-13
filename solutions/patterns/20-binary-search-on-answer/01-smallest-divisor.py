def ship_within_days(weights: list[int], days: int) -> int:
    def ok(cap):
        need = 1
        load = 0
        for w in weights:
            if load + w > cap:
                need += 1
                load = 0
            load += w
        return need <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def always_ready() -> bool:
    return True
