from pathlib import Path

import typer

app = typer.Typer()


@app.callback()
def main() -> None:
    """CSV tools."""


def count_rows(path: Path) -> int:
    raise NotImplementedError


@app.command()
def count(path: Path) -> None:
    raise NotImplementedError
