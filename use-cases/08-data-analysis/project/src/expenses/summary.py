from pathlib import Path


def monthly(csv_path: Path) -> dict[str, dict[str, int]]:
    """Return {month: {category: total}} from a date,amount,memo CSV."""
    raise NotImplementedError


def chart(csv_path: Path, image_path: Path) -> None:
    """Write a bar chart of monthly totals."""
    raise NotImplementedError
