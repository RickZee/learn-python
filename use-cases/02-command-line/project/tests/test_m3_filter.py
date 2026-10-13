from csvtool.main import app, count_rows
from typer.testing import CliRunner

runner = CliRunner()


def test_where_filters_rows(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name,city\nada,Paris\nbea,Rome\ncy,Paris\n", encoding="utf-8")
    assert count_rows(path, ["city=Paris"]) == 2


def test_unknown_column_exits_2(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name\nada\n", encoding="utf-8")
    result = runner.invoke(app, ["count", str(path), "--where", "nope=1"])
    assert result.exit_code == 2
    assert "error: no column 'nope'" in result.stderr
