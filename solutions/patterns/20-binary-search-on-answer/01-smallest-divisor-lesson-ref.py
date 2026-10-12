def smallest_divisor(nums: list[int], threshold: int) -> int:
    def ok(d):
        return sum((x + d - 1) // d for x in nums) <= threshold
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
