import copy
import re


class PatchError(ValueError):
    pass


_IDX = re.compile(r"0|[1-9][0-9]*")


def _tokens(ptr):
    if not isinstance(ptr, str):
        raise PatchError("pointer must be a string")
    if ptr == "":
        return []
    if not ptr.startswith("/"):
        raise PatchError(f"bad pointer {ptr!r}")
    return [t.replace("~1", "/").replace("~0", "~") for t in ptr.split("/")[1:]]


def _index(lst, tok, allow_end):
    if tok == "-" and allow_end:
        return len(lst)
    if not _IDX.fullmatch(tok):
        raise PatchError(f"bad index {tok!r}")
    i = int(tok)
    if i > len(lst) or (i == len(lst) and not allow_end):
        raise PatchError(f"index out of range {tok!r}")
    return i


def _child(node, tok):
    if isinstance(node, dict):
        if tok not in node:
            raise PatchError(f"missing member {tok!r}")
        return node[tok]
    if isinstance(node, list):
        return node[_index(node, tok, allow_end=False)]
    raise PatchError("cannot descend into a scalar")


def _get(root, toks):
    node = root
    for t in toks:
        node = _child(node, t)
    return node


def _parent(root, toks):
    return _get(root, toks[:-1])


def _add(root, toks, value):
    if not toks:
        return value
    parent = _parent(root, toks)
    last = toks[-1]
    if isinstance(parent, dict):
        parent[last] = value
    elif isinstance(parent, list):
        parent.insert(_index(parent, last, allow_end=True), value)
    else:
        raise PatchError("cannot add into a scalar")
    return root


def _remove(root, toks):
    if not toks:
        raise PatchError("cannot remove the whole document")
    parent = _parent(root, toks)
    last = toks[-1]
    if isinstance(parent, dict):
        if last not in parent:
            raise PatchError(f"missing member {last!r}")
        return parent.pop(last)
    if isinstance(parent, list):
        return parent.pop(_index(parent, last, allow_end=False))
    raise PatchError("cannot remove from a scalar")


def _replace(root, toks, value):
    if not toks:
        return value
    _get(root, toks)
    parent = _parent(root, toks)
    last = toks[-1]
    if isinstance(parent, dict):
        parent[last] = value
    else:
        parent[_index(parent, last, allow_end=False)] = value
    return root


def _need(op, key):
    if key not in op:
        raise PatchError(f"missing {key!r}")
    return op[key]


def apply_patch(doc, patch):
    root = copy.deepcopy(doc)
    for op in patch:
        if not isinstance(op, dict):
            raise PatchError("operation must be an object")
        kind = _need(op, "op")
        toks = _tokens(_need(op, "path"))
        if kind == "add":
            root = _add(root, toks, copy.deepcopy(_need(op, "value")))
        elif kind == "remove":
            _remove(root, toks)
        elif kind == "replace":
            root = _replace(root, toks, copy.deepcopy(_need(op, "value")))
        elif kind == "test":
            if _get(root, toks) != _need(op, "value"):
                raise PatchError("test failed")
        elif kind in ("move", "copy"):
            src = _tokens(_need(op, "from"))
            if kind == "move":
                if len(src) < len(toks) and toks[: len(src)] == src and src != toks:
                    raise PatchError("cannot move into own descendant")
                value = _remove(root, src) if src else root
                root = _add(root, toks, value)
            else:
                root = _add(root, toks, copy.deepcopy(_get(root, src)))
        else:
            raise PatchError(f"unknown op {kind!r}")
    return root
