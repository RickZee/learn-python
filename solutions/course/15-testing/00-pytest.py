def positive(n: int) -> bool:
    return n > 0


def test_positive() -> None:
    assert positive(2) is True
    assert positive(0) is False


def test_signs() -> None:
    assert positive(1) is True
    assert positive(0) is False
    assert positive(-1) is False


def positive_count(nums: list[int]) -> int:
    return sum(1 for n in nums if n > 0)


def test_count() -> None:
    assert positive_count([1, 0, -2, 3]) == 2
    assert positive_count([]) == 0
