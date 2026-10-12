def min_eating_speed(piles: list[int], h: int) -> int:
    """Minimum integer eating speed to finish all piles within h hours.

    Approach: binary search speed; feasibility is sum of ceil(pile / speed).
    Time: O(n log M) for M = max(piles)
    Space: O(1)
    Alternative: try every speed from 1 to max(piles).
    Common bugs: float ceil on huge piles; wrong binary-search bound update.
    """

    def hours(speed):
        return sum((p + speed - 1) // speed for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
