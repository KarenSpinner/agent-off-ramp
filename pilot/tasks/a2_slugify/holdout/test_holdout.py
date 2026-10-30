from src.slugify import slugify


def test_double_space_spec():
    assert slugify("x  y") == "x-y"


def test_mixed():
    assert slugify("Mixed_Case  Here!!") == "mixed-case-here"
    assert slugify("p   q") == "p-q"
