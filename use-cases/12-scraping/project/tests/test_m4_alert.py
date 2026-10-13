from decimal import Decimal

from watch.prices import should_alert


def test_alert_on_ten_percent_drop():
    assert should_alert(Decimal("100"), Decimal("89"), 10) is True


def test_no_alert_on_small_drop():
    assert should_alert(Decimal("100"), Decimal("95"), 10) is False
