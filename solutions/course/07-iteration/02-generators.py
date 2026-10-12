
def once():
    yield 1


def first() -> int:
    return next(once())


def squares(nums: list[int]):
    for value in nums:
        yield value * value


def square_list(nums: list[int]) -> list[int]:
    return list(squares(nums))


def over_limit(readings: list[int], limit: int):
    for value in readings:
        if value > limit:
            yield value


def flagged(readings: list[int], limit: int) -> list[int]:
    return list(over_limit(readings, limit))
