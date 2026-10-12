from limiter.window import Window


def test_keys_do_not_share_counts():
    first = Window(limit=2)
    second = Window(limit=2)
    assert first.hit("ada")
    assert first.hit("ada")
    assert not first.hit("ada")
    assert second.hit("ada"), "second window shared the first window's counts"
