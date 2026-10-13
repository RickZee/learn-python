from __future__ import annotations

from pathlib import Path

import typer

from readinglist.store import BookStore, DuplicateIsbnError, InvalidStatusError

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
    store = BookStore(database)
    try:
        book = store.add(isbn, title=title)
    except DuplicateIsbnError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(str(book["id"]))


@app.command("list")
def list_books(
    status: str | None = typer.Option(None, "--status"),
    database: Path = typer.Option(Path("readinglist.db"), "--database"),
) -> None:
    store = BookStore(database)
    try:
        books = store.list(status=status)
    except InvalidStatusError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    for book in books:
        title = book["title"] if book["title"] else "-"
        typer.echo(f"{book['id']} {book['isbn']} {title}")


@app.command()
def mark(
    book_id: int,
    status: str,
    database: Path = typer.Option(Path("readinglist.db"), "--database"),
) -> None:
    store = BookStore(database)
    try:
        book = store.set_status(book_id, status)
    except InvalidStatusError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    if book is None:
        typer.echo(f"error: no book {book_id}", err=True)
        raise typer.Exit(code=2)
    typer.echo(f"{book['id']} {book['status']}")
