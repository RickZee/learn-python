import csv
import json
from pathlib import Path


def summarize(csv_path: str, json_path: str) -> None:
    """Read a CSV with columns name and qty. Write JSON {"rows": n, "qty": total}."""
    with Path(csv_path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    payload = {"rows": len(rows), "qty": sum(int(row["qty"]) for row in rows)}
    Path(json_path).write_text(json.dumps(payload), encoding="utf-8")
