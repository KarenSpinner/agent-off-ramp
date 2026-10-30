import re


class PatchError(ValueError):
    pass


_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _split(text):
    if text == "":
        return [], True
    trailing = text.endswith("\n")
    lines = text.split("\n")
    if trailing:
        lines.pop()
    return lines, trailing


def _hunks(patch):
    plines = patch.split("\n")
    if plines and plines[-1] == "":
        plines.pop()
    hunks, cur = [], None
    for raw in plines:
        if raw.startswith("\\"):
            continue
        m = _HUNK.match(raw)
        if m:
            cur = {"a": int(m.group(1)), "b": int(m.group(2) or 1),
                   "d": int(m.group(4) or 1), "body": []}
            hunks.append(cur)
            continue
        if cur is None:
            if raw.startswith("--- ") or raw.startswith("+++ "):
                continue
            raise PatchError(f"unexpected line outside hunk: {raw!r}")
        if raw == "":
            cur["body"].append((" ", ""))
        elif raw[0] in " -+":
            cur["body"].append((raw[0], raw[1:]))
        else:
            raise PatchError(f"malformed hunk line: {raw!r}")
    return hunks


def apply_unified(text: str, patch: str) -> str:
    lines, trailing = _split(text)
    out = list(lines)
    offset = 0
    for h in _hunks(patch):
        body = h["body"]
        old = [t for k, t in body if k in " -"]
        new = [t for k, t in body if k in " +"]
        if len(old) != h["b"] or len(new) != h["d"]:
            raise PatchError("hunk counts do not match body")
        if h["b"] == 0:
            pos = h["a"] + offset
        else:
            if h["a"] == 0:
                raise PatchError("old start must be >= 1 when lines are removed or kept")
            pos = h["a"] - 1 + offset
        if pos < 0 or pos + len(old) > len(out):
            raise PatchError("hunk reaches past end of file")
        if out[pos:pos + len(old)] != old:
            raise PatchError("context mismatch")
        out[pos:pos + len(old)] = new
        offset += len(new) - len(old)
    return "\n".join(out) + ("\n" if trailing else "")
