from pylearn import load_exercise

wraps = load_exercise("wraps")


@wraps.shout
def greet(name: str) -> str:
    return name


def test_shout_uppercases():
    assert greet("ab") == "AB"


def test_wraps_keeps_the_name():
    assert greet.__name__ == "greet"
