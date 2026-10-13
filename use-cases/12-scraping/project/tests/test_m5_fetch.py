from decimal import Decimal

import httpx
from watch.prices import fetch_price


def test_fetch_price_with_mock_transport():
    html = '<html><span class="price">$12.50</span></html>'

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=html)

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        assert fetch_price(client, "https://example.test/item") == Decimal("12.50")


def test_fetch_price_missing():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html></html>")

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        assert fetch_price(client, "https://example.test/item") is None
