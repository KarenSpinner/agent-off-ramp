import pytest

from src.unidiff import PatchError, apply_unified

A = "alpha\nbeta\ngamma\ndelta\nepsilon\n"


def test_replace_one_line():
    p = "@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n"
    assert apply_unified(A, p) == "alpha\nBETA\ngamma\ndelta\nepsilon\n"


def test_two_hunks_with_offset():
    p = ("@@ -1,2 +1,3 @@\n alpha\n+inserted\n beta\n"
         "@@ -4,2 +5,2 @@\n delta\n-epsilon\n+EPSILON\n")
    assert apply_unified(A, p) == "alpha\ninserted\nbeta\ngamma\ndelta\nEPSILON\n"


def test_context_mismatch():
    with pytest.raises(PatchError):
        apply_unified(A, "@@ -1,2 +1,2 @@\n beta\n alpha\n")


def test_count_mismatch():
    with pytest.raises(PatchError):
        apply_unified(A, "@@ -1,2 +1,2 @@\n alpha\n beta\n gamma\n")


def test_insert_into_empty_file():
    assert apply_unified("", "@@ -0,0 +1,2 @@\n+a\n+b\n") == "a\nb\n"


def test_delete_lines():
    assert apply_unified(A, "@@ -2,2 +2,0 @@\n-beta\n-gamma\n") == "alpha\ndelta\nepsilon\n"


def test_headers_defaults_and_marker():
    p = "--- a/f.txt\n+++ b/f.txt\n@@ -5 +5 @@\n-epsilon\n+omega\n\\ No newline at end of file\n"
    assert apply_unified(A, p) == "alpha\nbeta\ngamma\ndelta\nomega\n"


def test_hunk_past_end():
    with pytest.raises(PatchError):
        apply_unified(A, "@@ -9,1 +9,1 @@\n-x\n+y\n")


def test_pure_insertion_after_line():
    assert apply_unified(A, "@@ -3,0 +4,1 @@\n+middle\n") == "alpha\nbeta\ngamma\nmiddle\ndelta\nepsilon\n"


def test_preserves_missing_trailing_newline():
    assert apply_unified("a\nb", "@@ -2 +2 @@\n-b\n+c\n") == "a\nc"


def test_malformed_lines():
    with pytest.raises(PatchError):
        apply_unified(A, "@@ -1 +1 @@\nxalpha\n")
    with pytest.raises(PatchError):
        apply_unified(A, "hello\n@@ -1 +1 @@\n alpha\n")
