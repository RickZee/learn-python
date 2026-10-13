import json

from csvtool.main import app, summarize
from typer.testing import CliRunner

runner = CliRunner()


def test_summarize_skips_blanks(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("name,qty\na,1\nb,\nc,3\n", encoding="utf-8")
    stats = summarize(path, "qty")
    assert stats["count"] == 2
    assert stats["blanks"] == 1
    assert stats["min"] == 1
    assert stats["max"] == 3
    assert stats["mean"] == 2.0


def test_summary_json(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("qty\n2\n4\n", encoding="utf-8")
    result = runner.invoke(app, ["summary", str(path), "qty", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["count"] == 2
    assert data["mean"] == 3.0


def test_non_number_exits_2(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("qty\n1\nx\n", encoding="utf-8")
    result = runner.invoke(app, ["summary", str(path), "qty"])
    assert result.exit_code == 2
    assert "error: non-number in row" in result.stderr
