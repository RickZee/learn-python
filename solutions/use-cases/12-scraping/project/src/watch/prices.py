from __future__ import annotations

import re
import sqlite3
import time
from decimal import Decimal
from pathlib import Path

from bs4 import BeautifulSoup

PRICE_RE = re.compile(r"([0-9][0-9.,]*)")


def parse_price(html: str) -> Decimal | None:
    node = BeautifulSoup(html, "html.parser").select_one(".price")
    if node is None:
        return None
    text = node.get_text(strip=True)
    match = PRICE_RE.search(text)
    if match is None:
        return None
    raw = match.group(1)
    if "," in raw and "." in raw:
        if raw.rfind(",") > raw.rfind("."):
            raw = raw.replace(".", "").replace(",", ".")
        else:
            raw = raw.replace(",", "")
    elif "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    else:
        raw = raw.replace(",", "")
    return Decimal(raw)


def _connect(database: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database)
    connection.execute(
        "create table if not exists prices (id integer primary key, item_id text, price text)"
    )
    return connection


def record_price(database: Path, item_id: str, price: Decimal) -> None:
    connection = _connect(database)
    connection.execute("insert into prices (item_id, price) values (?, ?)", (item_id, str(price)))
    connection.commit()
    connection.close()


def last_price(database: Path, item_id: str) -> Decimal | None:
    connection = _connect(database)
    row = connection.execute(
        "select price from prices where item_id = ? order by id desc limit 1",
        (item_id,),
    ).fetchone()
    connection.close()
    return None if row is None else Decimal(row[0])


def should_alert(previous: Decimal, current: Decimal, percent: float) -> bool:
    if previous <= 0:
        return False
    drop = (previous - current) / previous * Decimal("100")
    return drop >= Decimal(str(percent))


def fetch_price(client, url: str) -> Decimal | None:
    time.sleep(0.01)
    response = client.get(url)
    response.raise_for_status()
    return parse_price(response.text)
