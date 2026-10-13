from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class Row:
    date: str
    amount: Decimal
    memo: str


def parse_rows(csv_path: Path) -> tuple[list[Row], list[str]]:
    """Return (good rows, error messages with line numbers)."""
    raise NotImplementedError


def categorize(rows: list[Row], rules_path: Path) -> list[tuple[Row, str]]:
    """Attach a category name to each row using rules JSON {memo: category}."""
    raise NotImplementedError


def monthly_totals(categorized: list[tuple[Row, str]]) -> dict[str, dict[str, Decimal]]:
    """Return {month: {category: total}}."""
    raise NotImplementedError


def over_budget(
    totals: dict[str, dict[str, Decimal]], budget_path: Path
) -> list[tuple[str, str, Decimal, Decimal]]:
    """Return (month, category, spent, limit) for over-budget cells."""
    raise NotImplementedError


def chart(csv_path: Path, image_path: Path, rules_path: Path) -> None:
    """Write a bar chart of monthly totals (optional M5 helper)."""
    raise NotImplementedError
