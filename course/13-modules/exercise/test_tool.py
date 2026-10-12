import subprocess
import sys

from pylearn import load_exercise


def test_import_prints_nothing(capsys):
    load_exercise("tool")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_running_the_file_prints_hello():
    tool = load_exercise("tool")
    result = subprocess.run([sys.executable, tool.__file__], capture_output=True, text=True)
    assert result.stdout == "hello from tool\n"
