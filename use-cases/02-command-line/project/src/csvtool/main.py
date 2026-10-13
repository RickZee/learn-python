from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer(add_completion=False)


@app.callback()
def main() -> None:
    """CSV tools."""


def count_rows(path: Path, wheres: list[str] | None = None) -> int:
    raise NotImplementedError


def column_names(path: Path) -> list[str]:
    raise NotImplementedError


def summarize(path: Path, column: str) -> dict[str, float | int]:
    raise NotImplementedError


@app.command()
def count(
    path: Path,
    where: list[str] = typer.Option(None, "--where", help="COL=VALUE, repeatable"),
) -> None:
    """Print the number of data rows."""
    raise NotImplementedError


@app.command()
def columns(path: Path) -> None:
    """Print header names, numbered from 1."""
    raise NotImplementedError


@app.command()
def summary(
    path: Path,
    column: str,
    as_json: bool = typer.Option(False, "--json", help="Print JSON instead of text"),
) -> None:
    """Print count, min, max, and mean for a numeric column."""
    raise NotImplementedError
