import csv
import io


def total_qty(text: str) -> int:
    rows = csv.DictReader(io.StringIO(text))
    return sum(int(row["qty"]) for row in rows)


def qty_sum(text: str) -> int:
    return total_qty(text)


def order_count(text: str) -> int:
    rows = csv.DictReader(io.StringIO(text))
    total = 0
    for _ in rows:
        total += 1
    return total


def open_csv_kwargs() -> dict:
    return {"encoding": "utf-8", "newline": ""}
