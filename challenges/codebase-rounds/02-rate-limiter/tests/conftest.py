"""Import the stub package, or the reference solution when PYLEARN_SOLUTIONS=1."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROUND = Path(__file__).resolve().parents[1]
REPO = ROUND.parents[2]
FOLDER = ROUND
if os.environ.get("PYLEARN_SOLUTIONS") == "1":
    FOLDER = REPO / "solutions" / ROUND.relative_to(REPO)
sys.path.insert(0, str(FOLDER))
