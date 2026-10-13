from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Row:
    date: str
    amount: Decimal
    memo: str


def parse_rows(csv_path: Path) -> tuple[list[Row], list[str]]:
    rows: list[Row] = []
    errors: list[str] = []
    with csv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for index, raw in enumerate(reader, start=2):
            try:
                amount = Decimal(raw["amount"])
                rows.append(Row(date=raw["date"], amount=amount, memo=raw["memo"]))
            except (KeyError, InvalidOperation) as exc:
                errors.append(f"line {index}: {exc}")
    return rows, errors


def categorize(rows: list[Row], rules_path: Path) -> list[tuple[Row, str]]:
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    return [(row, rules.get(row.memo, "other")) for row in rows]


def monthly_totals(categorized: list[tuple[Row, str]]) -> dict[str, dict[str, Decimal]]:
    result: dict[str, dict[str, Decimal]] = {}
    for row, category in categorized:
        month = row.date[:7]
        bucket = result.setdefault(month, {})
        bucket[category] = bucket.get(category, Decimal("0")) + row.amount
    return result


def over_budget(
    totals: dict[str, dict[str, Decimal]], budget_path: Path
) -> list[tuple[str, str, Decimal, Decimal]]:
    budget = {
        key: Decimal(str(value))
        for key, value in json.loads(budget_path.read_text(encoding="utf-8")).items()
    }
    hits: list[tuple[str, str, Decimal, Decimal]] = []
    for month, cats in totals.items():
        for category, spent in cats.items():
            limit = budget.get(category)
            if limit is not None and spent > limit:
                hits.append((month, category, spent, limit))
    return hits


def chart(csv_path: Path, image_path: Path, rules_path: Path) -> None:
    rows, _ = parse_rows(csv_path)
    categorized = categorize(rows, rules_path)
    totals = monthly_totals(categorized)
    months = sorted(totals)
    values = [float(sum(totals[month].values())) for month in months]
    figure, axes = plt.subplots()
    axes.bar(months, values)
    figure.savefig(image_path)
    plt.close(figure)
