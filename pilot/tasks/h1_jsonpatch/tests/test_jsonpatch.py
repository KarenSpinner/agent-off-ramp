import pytest

from src.jsonpatch import PatchError, apply_patch


def test_add_member_and_replace_existing():
    assert apply_patch({"a": 1}, [{"op": "add", "path": "/b", "value": 2}]) == {"a": 1, "b": 2}
    assert apply_patch({"a": 1}, [{"op": "add", "path": "/a", "value": 3}]) == {"a": 3}


def test_add_array_index_and_append():
    assert apply_patch({"l": [1, 3]}, [{"op": "add", "path": "/l/1", "value": 2}]) == {"l": [1, 2, 3]}
    assert apply_patch({"l": [1]}, [{"op": "add", "path": "/l/-", "value": 2}]) == {"l": [1, 2]}
    assert apply_patch({"l": [1]}, [{"op": "add", "path": "/l/1", "value": 2}]) == {"l": [1, 2]}


def test_remove():
    assert apply_patch({"a": 1, "b": 2}, [{"op": "remove", "path": "/b"}]) == {"a": 1}
    assert apply_patch({"l": [1, 2, 3]}, [{"op": "remove", "path": "/l/0"}]) == {"l": [2, 3]}


def test_replace_requires_existing():
    assert apply_patch({"a": 1}, [{"op": "replace", "path": "/a", "value": 2}]) == {"a": 2}
    with pytest.raises(PatchError):
        apply_patch({"a": 1}, [{"op": "replace", "path": "/b", "value": 2}])


def test_move():
    doc = {"a": {"b": 1}, "c": {}}
    assert apply_patch(doc, [{"op": "move", "from": "/a/b", "path": "/c/d"}]) == {"a": {}, "c": {"d": 1}}
    with pytest.raises(PatchError):
        apply_patch({"a": {"x": 1}}, [{"op": "move", "from": "/a", "path": "/a/b"}])


def test_copy_is_independent():
    out = apply_patch({"a": [1, 2]}, [{"op": "copy", "from": "/a", "path": "/b"}])
    assert out == {"a": [1, 2], "b": [1, 2]}
    out["b"].append(3)
    assert out["a"] == [1, 2]


def test_test_op():
    assert apply_patch({"a": 1}, [{"op": "test", "path": "/a", "value": 1}]) == {"a": 1}
    with pytest.raises(PatchError):
        apply_patch({"a": 1}, [{"op": "test", "path": "/a", "value": 2}])


def test_pointer_escapes():
    doc = {"a/b": 1, "m~n": 2}
    assert apply_patch(doc, [{"op": "replace", "path": "/a~1b", "value": 9}]) == {"a/b": 9, "m~n": 2}
    assert apply_patch(doc, [{"op": "remove", "path": "/m~0n"}]) == {"a/b": 1}


def test_whole_document_and_no_mutation():
    doc = {"a": 1}
    assert apply_patch(doc, [{"op": "replace", "path": "", "value": {"x": 1}}]) == {"x": 1}
    assert apply_patch(doc, [{"op": "add", "path": "/b", "value": [1]}])["b"] == [1]
    assert doc == {"a": 1}


def test_atomic_failure_leaves_input_unchanged():
    doc = {"a": 1}
    with pytest.raises(PatchError):
        apply_patch(doc, [{"op": "add", "path": "/b", "value": 2}, {"op": "remove", "path": "/zzz"}])
    assert doc == {"a": 1}


def test_bad_pointers_and_indices():
    for bad in ("a", "/l/5", "/l/x", "/l/01"):
        with pytest.raises(PatchError):
            apply_patch({"l": [1]}, [{"op": "add", "path": bad, "value": 0}])
    with pytest.raises(PatchError):
        apply_patch({"a": 1}, [{"op": "frobnicate", "path": "/a"}])
    with pytest.raises(PatchError):
        apply_patch({"a": 1}, [{"op": "add", "path": "/b"}])
