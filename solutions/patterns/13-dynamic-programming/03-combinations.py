def fewest_ones(amount: int) -> int:
    return amount


def combinations(coins: list[int], amount: int) -> int:
    """Return how many unordered combinations of coins sum to amount.

    Approach: for each coin, add ways to make each total that can take that coin.
    Time: O(amount * coins)
    Space: O(amount)
    Alternative: recursion with memoization.
    Common bugs: counting permutations instead of combinations.
    """
    ways = [0] * (amount + 1)
    ways[0] = 1
    for coin in coins:
        for total in range(coin, amount + 1):
            ways[total] += ways[total - coin]
    return ways[amount]


def can_make(coins: list[int], amount: int) -> bool:
    possible = {0}
    for coin in coins:
        possible |= {total + coin for total in possible if total + coin <= amount}
        # Repeat so one coin can be used more than once.
        grew = True
        while grew:
            added = {total + coin for total in possible if total + coin <= amount} - possible
            possible |= added
            grew = bool(added)
    return amount in possible
