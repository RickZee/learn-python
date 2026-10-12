def squares(n: int) -> list[int]:
    return [value * value for value in range(n)]


def even_squares(n: int) -> list[int]:
    return [value * value for value in range(n) if value % 2 == 0]


def under_budget(prices: list[int], limit: int) -> list[int]:
    return [price for price in prices if price < limit]
