from src.dedupe import dedupe


def test_sorted_input():
    assert dedupe([1, 2, 2, 3]) == [1, 2, 3]


def test_order_preserved():
    assert dedupe([3, 1, 3, 2]) == [3, 1, 2]


def test_is_sorted():
    out = dedupe([3, 1, 3, 2])
    assert out == sorted(out)


def test_empty():
    assert dedupe([]) == []
