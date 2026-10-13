from __future__ import annotations

import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

import typer

app = typer.Typer(add_completion=False)


class CsvToolError(Exception):
    """User-facing CSV failure."""


@app.callback()
def main() -> None:
    """CSV tools."""


def _open_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise CsvToolError(f"error: missing file '{path}'")
    text = path.read_text(encoding="utf-8")
    if text == "":
        raise CsvToolError("error: empty file")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise CsvToolError("error: empty file")
        fieldnames = list(reader.fieldnames)
        rows: list[dict[str, str]] = []
        for index, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise CsvToolError(f"error: ragged row {index}")
            if len(row) != len(fieldnames):
                raise CsvToolError(f"error: ragged row {index}")
            rows.append(dict(row))
    return fieldnames, rows


def count_rows(path: Path, wheres: list[str] | None = None) -> int:
    fieldnames, rows = _open_rows(path)
    filters = _parse_wheres(wheres or [], fieldnames)
    return sum(1 for row in rows if _matches(row, filters))


def column_names(path: Path) -> list[str]:
    fieldnames, _ = _open_rows(path)
    return fieldnames


def summarize(path: Path, column: str) -> dict[str, float | int]:
    fieldnames, rows = _open_rows(path)
    if column not in fieldnames:
        raise CsvToolError(f"error: no column '{column}'")
    values: list[Decimal] = []
    blanks = 0
    for index, row in enumerate(rows, start=2):
        raw = row[column].strip()
        if raw == "":
            blanks += 1
            continue
        try:
            values.append(Decimal(raw))
        except InvalidOperation as exc:
            raise CsvToolError(f"error: non-number in row {index}") from exc
    if not values:
        return {"count": 0, "blanks": blanks, "min": 0, "max": 0, "mean": 0.0}
    total = sum(values)
    return {
        "count": len(values),
        "blanks": blanks,
        "min": float(min(values)),
        "max": float(max(values)),
        "mean": float(total / len(values)),
    }


def _parse_wheres(wheres: list[str], fieldnames: list[str]) -> list[tuple[str, str]]:
    filters: list[tuple[str, str]] = []
    for item in wheres:
        if "=" not in item:
            raise CsvToolError(f"error: bad filter '{item}'")
        column, value = item.split("=", 1)
        if column not in fieldnames:
            raise CsvToolError(f"error: no column '{column}'")
        filters.append((column, value))
    return filters


def _matches(row: dict[str, str], filters: list[tuple[str, str]]) -> bool:
    return all(row.get(column) == value for column, value in filters)


@app.command()
def count(
    path: Path,
    where: list[str] = typer.Option(None, "--where", help="COL=VALUE, repeatable"),
) -> None:
    """Print the number of data rows."""
    try:
        typer.echo(str(count_rows(path, where or [])))
    except CsvToolError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@app.command()
def columns(path: Path) -> None:
    """Print header names, numbered from 1."""
    try:
        names = column_names(path)
    except CsvToolError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    for index, name in enumerate(names, start=1):
        typer.echo(f"{index}. {name}")


@app.command()
def summary(
    path: Path,
    column: str,
    as_json: bool = typer.Option(False, "--json", help="Print JSON instead of text"),
) -> None:
    """Print count, min, max, and mean for a numeric column."""
    try:
        stats = summarize(path, column)
    except CsvToolError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    if as_json:
        typer.echo(json.dumps(stats))
        return
    typer.echo(f"count={stats['count']}")
    typer.echo(f"blanks={stats['blanks']}")
    typer.echo(f"min={stats['min']}")
    typer.echo(f"max={stats['max']}")
    typer.echo(f"mean={stats['mean']}")
