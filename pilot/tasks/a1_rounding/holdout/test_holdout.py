from src.rounding import round_half_up


def test_small_tie_spec():
    assert round_half_up(0.125, 2) == 0.13


def test_more_ties():
    assert round_half_up(2.675, 2) == 2.68
    assert round_half_up(-0.125, 2) == -0.13
    assert round_half_up(7.5) == 8
