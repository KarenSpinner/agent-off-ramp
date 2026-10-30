from src.rounding import round_half_up


def test_ties_away_from_zero():
    assert round_half_up(2.5) == 3


def test_negative_ties():
    assert round_half_up(-2.5) == -3


def test_two_digits():
    assert round_half_up(0.375, 2) == 0.38


def test_float_artifact():
    assert round_half_up(1.005, 2) == 1.01


def test_small_tie():
    assert round_half_up(0.125, 2) == 0.12


def test_integer_passthrough():
    assert round_half_up(3.0) == 3.0
