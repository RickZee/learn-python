import subprocess
import sys

from pylearn import load_exercise


def test_script_prints_squares():
    module = load_exercise("squares")
    result = subprocess.run([sys.executable, module.__file__], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout == "[1, 4, 9]\n"
