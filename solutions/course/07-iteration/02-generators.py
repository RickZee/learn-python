def once():
    yield 1


def first() -> int:
    return next(once())


def squares(nums: list[int]):
    for value in nums:
        yield value * value


def square_list(nums: list[int]) -> list[int]:
    return list(squares(nums))


def sum_twice(nums: list[int]) -> tuple[int, int]:
    def gen():
        for n in nums:
            yield n * n

    first = sum(gen())
    second = sum(gen())
    return first, second


def over_limit(readings: list[int], limit: int):
    for value in readings:
        if value > limit:
            yield value
