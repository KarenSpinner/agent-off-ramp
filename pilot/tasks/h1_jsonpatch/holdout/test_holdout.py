import pytest

from src.jsonpatch import PatchError, apply_patch


def test_more():
    with pytest.raises(PatchError):
        apply_patch({"l": [1]}, [{"op": "remove", "path": "/l/-"}])
    assert apply_patch({"l": [1, 2, 3]}, [{"op": "move", "from": "/l/0", "path": "/l/2"}]) == {"l": [2, 3, 1]}
    assert apply_patch({"l": [1, 2]}, [{"op": "test", "path": "/l/1", "value": 2}]) == {"l": [1, 2]}
    assert apply_patch({"a": {"b": {"c": 1}}}, [{"op": "remove", "path": "/a/b/c"}]) == {"a": {"b": {}}}
    with pytest.raises(PatchError):
        apply_patch({"a": 1}, [{"op": "remove", "path": ""}])
