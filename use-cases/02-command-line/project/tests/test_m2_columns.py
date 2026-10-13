from csvtool.main import app, column_names
from typer.testing import CliRunner

runner = CliRunner()


def test_column_names_reads_header(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name,qty\nada,1\n", encoding="utf-8")
    assert column_names(path) == ["name", "qty"]


def test_cli_numbers_from_one(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name,qty\nada,1\n", encoding="utf-8")
    result = runner.invoke(app, ["columns", str(path)])
    assert result.exit_code == 0
    assert "1. name" in result.stdout
    assert "2. qty" in result.stdout
