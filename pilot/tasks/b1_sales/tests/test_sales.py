import os

from src.sales import revenue_by_region

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sales_2025.csv")


def test_regions():
    r = revenue_by_region(DATA)
    assert set(r) == {"North", "South", "East", "West"}


def test_totals():
    r = revenue_by_region(DATA)
    assert r["North"] == 48213.75
    assert r["South"] == 39977.10
    assert r["East"] == 51102.00
    assert r["West"] == 27460.45


def test_rounding():
    r = revenue_by_region(DATA)
    assert all(round(v, 2) == v for v in r.values())
