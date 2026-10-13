from csvtool.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_missing_file_exits_2(tmp_path):
    path = tmp_path / "missing.csv"
    result = runner.invoke(app, ["count", str(path)])
    assert result.exit_code == 2
    assert "error: missing file" in result.stderr
    assert (
        result.exception is None
        or not isinstance(result.exception, Exception)
        or "Traceback" not in (result.stdout + result.stderr)
    )


def test_empty_file_exits_2(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    result = runner.invoke(app, ["count", str(path)])
    assert result.exit_code == 2
    assert "error: empty file" in result.stderr


def test_ragged_row_exits_2(tmp_path):
    path = tmp_path / "ragged.csv"
    path.write_text("name,qty\nada\n", encoding="utf-8")
    result = runner.invoke(app, ["count", str(path)])
    assert result.exit_code == 2
    assert "error: ragged row" in result.stderr
