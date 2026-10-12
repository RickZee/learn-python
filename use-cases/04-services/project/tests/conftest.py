import os
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[2]
SRC = PROJECT / "src"
if os.environ.get("PYLEARN_SOLUTIONS") == "1":
    SRC = REPO / "solutions" / PROJECT.relative_to(REPO) / "src"
sys.path.insert(0, str(SRC))
