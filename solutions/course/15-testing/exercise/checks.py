def check_word_count(word_count) -> None:
    assert word_count("") == 0
    assert word_count("one") == 1
    assert word_count("  two  words ") == 2


def check_shout(shout) -> None:
    assert shout("ab") == "AB"


def check_first_word(first_word) -> None:
    assert first_word("") == ""
    assert first_word("a b") == "a"
