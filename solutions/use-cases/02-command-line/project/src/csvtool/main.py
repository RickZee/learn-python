from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.callback()
def main() -> None:
    """CSV tools."""


def count_rows(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    return max(len(lines) - 1, 0)


@app.command()
def count(path: Path) -> None:
    console.print(str(count_rows(path)))
