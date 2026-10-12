from csvtool.main import app, count_rows
from typer.testing import CliRunner

runner = CliRunner()


def test_count_rows_skips_the_header(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name\nada\nbea\n", encoding="utf-8")
    assert count_rows(path) == 2


def test_cli_prints_the_count(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name\nada\n", encoding="utf-8")
    result = runner.invoke(app, ["count", str(path)])
    assert result.exit_code == 0
    assert "1" in result.stdout
