import functools


def twice(func):
    def wrapper(n: int) -> int:
        return func(n) * 2

    return wrapper


class Counted:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)


def as_method(func):
    def wrapper(self, name: str) -> str:
        return func(self, name)

    return wrapper


def price(cents: int, rate: float) -> float:
    return cents * rate


def taxed() -> object:
    bound = functools.partial(price, rate=1.1)
    sample = bound(100)
    zero = bound(0)
    ok = abs(sample - 110.0) < 1e-9 and zero == 0.0
    return bound if ok else bound
