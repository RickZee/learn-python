from pathlib import Path

from readinglist.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_add_prints_id(tmp_path: Path):
    database = tmp_path / "books.db"
    result = runner.invoke(
        app, ["add", "9780000000001", "--title", "Alpha", "--database", str(database)]
    )
    assert result.exit_code == 0
    assert result.stdout.strip() == "1"


def test_cli_list_and_duplicate(tmp_path: Path):
    database = tmp_path / "books.db"
    runner.invoke(app, ["add", "9780000000001", "--database", str(database)])
    listed = runner.invoke(app, ["list", "--database", str(database)])
    assert listed.exit_code == 0
    assert "9780000000001" in listed.stdout
    assert "-" in listed.stdout
    dup = runner.invoke(app, ["add", "9780000000001", "--database", str(database)])
    assert dup.exit_code == 2
    assert "duplicate isbn" in dup.stderr
