
import csv
import io


def total_qty(text: str) -> int:
    rows = csv.DictReader(io.StringIO(text))
    return sum(int(row["qty"]) for row in rows)


def qty_sum(text: str) -> int:
    return total_qty(text)


def order_count(text: str) -> int:
    rows = csv.DictReader(io.StringIO(text))
    return sum(1 for _ in rows)
