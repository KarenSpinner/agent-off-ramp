import pytest

from src.intervals import merge


def test_overlap():
    assert merge(["[1,3]", "[2,5]"]) == ["[1,5]"]


def test_touch_inclusive():
    assert merge(["[1,3)", "[3,5]"]) == ["[1,5]"]


def test_touch_exclusive_both():
    assert merge(["[1,3)", "(3,5]"]) == ["[1,3)", "(3,5]"]


def test_touch_keeps_exclusive_end():
    assert merge(["[1,3)", "[3,5)"]) == ["[1,5)"]


def test_unsorted_and_mixed_starts():
    assert merge(["(1,4]", "[1,2)"]) == ["[1,4]"]


def test_disjoint_groups():
    assert merge(["[5,6]", "[1,2]", "[2,3]"]) == ["[1,3]", "[5,6]"]


def test_point_interval():
    assert merge(["[1,1]", "(1,2)"]) == ["[1,2)"]


def test_empty_input():
    assert merge([]) == []


def test_invalid():
    with pytest.raises(ValueError):
        merge(["[3,1]"])
    with pytest.raises(ValueError):
        merge(["(2,2)"])
    with pytest.raises(ValueError):
        merge(["1,2"])
