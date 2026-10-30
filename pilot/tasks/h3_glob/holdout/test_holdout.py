from src.globmatch import match


def test_more():
    assert match("[a-]x", "-x")
    assert match("*", "")
    assert match("**/*.txt", "notes.txt")
    assert match("**/*.txt", "a/b/notes.txt")
    assert not match("[!]a]b", "]b")
    assert match("a/**/**/b", "a/b")
    assert not match("a/**/b", "a/b/c")
