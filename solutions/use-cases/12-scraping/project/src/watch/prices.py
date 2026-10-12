import sqlite3
from pathlib import Path

from bs4 import BeautifulSoup


def parse_price(html: str) -> str:
    node = BeautifulSoup(html, "html.parser").select_one(".price")
    if node is None or node.string is None:
        raise ValueError("no price")
    return node.string.strip()


def remember(database: Path, html: str) -> str:
    connection = sqlite3.connect(database)
    connection.execute("create table if not exists prices (id integer primary key, price text)")
    row = connection.execute("select price from prices order by id limit 1").fetchone()
    if row is not None:
        connection.close()
        return row[0]
    price = parse_price(html)
    connection.execute("insert into prices (price) values (?)", (price,))
    connection.commit()
    connection.close()
    return price
