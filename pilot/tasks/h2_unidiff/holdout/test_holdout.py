import pytest

from src.unidiff import PatchError, apply_unified

A = "alpha\nbeta\ngamma\ndelta\nepsilon\n"


def test_more():
    p = "@@ -1,5 +1,5 @@\n-alpha\n+ALPHA\n beta\n gamma\n delta\n-epsilon\n+EPSILON\n"
    assert apply_unified(A, p) == "ALPHA\nbeta\ngamma\ndelta\nEPSILON\n"
    assert apply_unified("x\n\ny\n", "@@ -1,3 +1,3 @@\n x\n\n-y\n+z\n") == "x\n\nz\n"
    with pytest.raises(PatchError):
        apply_unified(A, "@@ -0,1 +1,1 @@\n-alpha\n+a\n")
    assert apply_unified(A, "") == A
