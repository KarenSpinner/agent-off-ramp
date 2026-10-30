from datetime import datetime as dt

import pytest

from src.cronlite import next_run


def test_next_minute():
    assert next_run("* * *", dt(2025, 1, 1, 10, 30)) == dt(2025, 1, 1, 10, 31)


def test_seconds_dropped_strictly_after():
    assert next_run("* * *", dt(2025, 1, 1, 10, 30, 45)) == dt(2025, 1, 1, 10, 31)


def test_top_of_hour():
    assert next_run("0 * *", dt(2025, 1, 1, 10, 30)) == dt(2025, 1, 1, 11, 0)


def test_midnight():
    assert next_run("0 0 *", dt(2025, 1, 1, 10, 30)) == dt(2025, 1, 2, 0, 0)


def test_exact_match_rolls_to_next_month():
    assert next_run("30 9 15", dt(2025, 1, 15, 9, 30)) == dt(2025, 2, 15, 9, 30)


def test_year_wrap():
    assert next_run("0 0 1", dt(2025, 12, 31, 23, 59)) == dt(2026, 1, 1, 0, 0)


def test_daily_time():
    assert next_run("15 14 *", dt(2025, 3, 10, 14, 15)) == dt(2025, 3, 11, 14, 15)


def test_skip_short_month():
    assert next_run("0 12 31", dt(2025, 1, 31, 12, 0)) == dt(2025, 3, 31, 12, 0)


def test_invalid_specs():
    for bad in ("60 * *", "* * 0", "a b c", "* *", "* 24 *", "* * 32"):
        with pytest.raises(ValueError):
            next_run(bad, dt(2025, 1, 1))


def test_month_without_day():
    assert next_run("0 0 31", dt(2025, 4, 1)) == dt(2025, 4, 30)
