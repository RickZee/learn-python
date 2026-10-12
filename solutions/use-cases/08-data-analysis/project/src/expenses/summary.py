from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import polars as pl

RULES = {"coffee": "food", "rent": "home"}


def monthly(csv_path: Path) -> dict[str, dict[str, int]]:
    frame = pl.read_csv(csv_path).with_columns(
        pl.col("date").str.slice(0, 7).alias("month"),
        pl.col("memo").replace_strict(RULES, default="other").alias("category"),
    )
    grouped = frame.group_by("month", "category").agg(pl.col("amount").sum())
    result: dict[str, dict[str, int]] = {}
    for row in grouped.iter_rows(named=True):
        result.setdefault(row["month"], {})[row["category"]] = int(row["amount"])
    return result


def chart(csv_path: Path, image_path: Path) -> None:
    totals = monthly(csv_path)
    months = sorted(totals)
    values = [sum(totals[month].values()) for month in months]
    figure, axes = plt.subplots()
    axes.bar(months, values)
    figure.savefig(image_path)
    plt.close(figure)
