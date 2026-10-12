def max_profit(prices: list[int]) -> int:
    """One buy and one later sell. No profitable trade means 0.

    Approach: track the lowest price so far and the best gain after it.
    Time: O(n)
    Space: O(1)
    Alternative: check every pair of days.
    Common bugs: selling before the buy, or returning a negative profit.
    """
    lowest = None
    best = 0
    for price in prices:
        if lowest is None or price < lowest:
            lowest = price
        elif price - lowest > best:
            best = price - lowest
    return best
