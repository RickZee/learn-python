def double(n: int) -> int:
    return n * 2


def greet(name: str) -> str:
    return "hello " + name


def split_bill(price: int, tip: int, people: int) -> int:
    total = price + tip
    share = total // people
    return share
