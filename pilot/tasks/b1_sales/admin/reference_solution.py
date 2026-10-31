import csv
from collections import defaultdict


def revenue_by_region(path: str) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            totals[row["region"]] += int(row["units"]) * float(row["unit_price"])
    return {k: round(v, 2) for k, v in totals.items()}
