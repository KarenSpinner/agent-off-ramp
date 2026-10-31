import pytest

from src.rpn import eval_rpn


def test_add():
    assert eval_rpn(["2", "3", "+"]) == 5


def test_compound():
    assert eval_rpn(["5", "1", "2", "+", "4", "*", "+", "3", "-"]) == 14


def test_division_truncates_toward_zero():
    assert eval_rpn(["7", "2", "/"]) == 3
    assert eval_rpn(["-7", "2", "/"]) == -3
    assert eval_rpn(["7", "-2", "/"]) == -3


def test_neg():
    assert eval_rpn(["7", "neg", "2", "/"]) == -3
    assert eval_rpn(["4", "neg", "neg"]) == 4


def test_div_zero():
    with pytest.raises(ZeroDivisionError):
        eval_rpn(["4", "0", "/"])


def test_underflow():
    with pytest.raises(ValueError):
        eval_rpn(["1", "+"])
    with pytest.raises(ValueError):
        eval_rpn(["neg"])


def test_leftover_and_bad_token():
    with pytest.raises(ValueError):
        eval_rpn(["1", "2"])
    with pytest.raises(ValueError):
        eval_rpn(["x"])
    with pytest.raises(ValueError):
        eval_rpn([])
