from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer(add_completion=False)


@app.callback()
def main() -> None:
    """Reading list CLI."""


@app.command()
def add(
    isbn: str,
    title: str | None = typer.Option(None, "--title"),
    database: Path = typer.Option(Path("readinglist.db"), "--database"),
) -> None:
    raise NotImplementedError


@app.command("list")
def list_books(
    status: str | None = typer.Option(None, "--status"),
    database: Path = typer.Option(Path("readinglist.db"), "--database"),
) -> None:
    raise NotImplementedError


@app.command()
def mark(
    book_id: int,
    status: str,
    database: Path = typer.Option(Path("readinglist.db"), "--database"),
) -> None:
    raise NotImplementedError
