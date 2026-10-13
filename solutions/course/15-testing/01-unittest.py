def positive(n: int) -> bool:
    return n > 0


def test_positive() -> None:
    assert positive(2) is True
    assert positive(0) is False
    assert positive(-1) is False


def is_even(n: int) -> bool:
    return n % 2 == 0


def test_even() -> None:
    assert is_even(2) is True
    assert is_even(3) is False
    assert is_even(0) is True


def evens(nums: list[int]) -> list[int]:
    return [n for n in nums if is_even(n)]


def test_evens() -> None:
    assert evens([1, 2, 3, 4]) == [2, 4]
    assert evens([]) == []
    assert evens([1, 3]) == []


def check_evens() -> bool:
    ok_happy = evens([2, 4]) == [2, 4]
    ok_empty = evens([]) == []
    ok_odds = evens([1, 3]) == []
    return ok_happy and ok_empty and ok_odds
