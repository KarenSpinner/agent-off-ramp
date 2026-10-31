from datetime import datetime as dt

from src.cronlite import next_run


def test_month_without_day_spec():
    assert next_run("0 0 31", dt(2025, 4, 1)) == dt(2025, 5, 31)


def test_leap_handling():
    assert next_run("0 0 29", dt(2025, 2, 1)) == dt(2025, 3, 29)
    assert next_run("0 0 29", dt(2024, 2, 1)) == dt(2024, 2, 29)
