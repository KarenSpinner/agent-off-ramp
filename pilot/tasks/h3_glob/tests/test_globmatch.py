from src.globmatch import match


def test_star_within_segment():
    assert match("*.py", "main.py")
    assert not match("*.py", "dir/main.py")
    assert not match("a*b", "a/b")


def test_question_mark():
    assert match("?at", "cat")
    assert not match("?at", "at")
    assert not match("a?b", "a/b")


def test_classes():
    assert match("[a-c]at", "bat")
    assert not match("[!a-c]at", "bat")
    assert match("[!a-c]at", "rat")
    assert match("[]]x", "]x")


def test_double_star_segments():
    assert match("src/**/test_*.py", "src/test_a.py")
    assert match("src/**/test_*.py", "src/a/b/test_a.py")
    assert not match("src/**/test_*.py", "src/a/b/main.py")
    assert match("**", "a/b/c")


def test_double_star_inside_segment_is_star():
    assert match("a**b", "axxb")
    assert not match("a**b", "a/b")


def test_unterminated_bracket_is_literal():
    assert match("a[b", "a[b")
    assert not match("a[b", "ab")


def test_anchored():
    assert not match("a", "a/b")
    assert not match("a/b", "a")
    assert match("a/*/c", "a/b/c")
    assert not match("a/*/c", "a/b/d/c")


def test_double_star_at_end():
    assert match("a/**", "a")
    assert match("a/**", "a/b/c")
