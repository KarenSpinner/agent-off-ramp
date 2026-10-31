from src.slugify import slugify


def test_simple():
    assert slugify("Hello World") == "hello-world"


def test_punctuation():
    assert slugify("Hello, World!") == "hello-world"


def test_collapse():
    assert slugify("a   b") == "a-b"


def test_underscores():
    assert slugify("snake_case_name") == "snake-case-name"


def test_strip():
    assert slugify("  --Trim me--  ") == "trim-me"


def test_double_space():
    assert slugify("Hello  World") == "hello--world"
