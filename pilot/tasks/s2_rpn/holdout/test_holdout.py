import pytest

from src.rpn import eval_rpn


def test_more():
    assert eval_rpn(["-9", "-4", "/"]) == 2
    assert eval_rpn(["0", "5", "/"]) == 0
    assert eval_rpn(["3", "4", "*", "neg", "2", "-"]) == -14
    with pytest.raises(ValueError):
        eval_rpn(["1", "2", "3", "+"])
