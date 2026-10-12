def coin_change(coins: list[int], amount: int) -> int:
    """Return the fewest coins that sum to amount, or -1. Amount 0 needs 0.

    Approach: for each amount, try every coin that fits and keep the minimum.
    Time: O(amount * number of coins)
    Space: O(amount)
    Alternative: breadth-first search on the remaining amount.
    Common bugs: starting the table at 0, so an impossible amount looks free.
    """
    fewest = [0] + [amount + 1] * amount
    for coin in coins:
        for value in range(coin, amount + 1):
            fewest[value] = min(fewest[value], fewest[value - coin] + 1)
    if fewest[amount] <= amount:
        return fewest[amount]
    return -1
