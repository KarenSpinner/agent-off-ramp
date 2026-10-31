import re
from functools import lru_cache


@lru_cache(maxsize=None)
def _seg_regex(seg: str):
    i, out = 0, ""
    while i < len(seg):
        c = seg[i]
        if c == "*":
            out += ".*"
            while i + 1 < len(seg) and seg[i + 1] == "*":
                i += 1
        elif c == "?":
            out += "."
        elif c == "[":
            j = i + 1
            neg = j < len(seg) and seg[j] == "!"
            if neg:
                j += 1
            if j < len(seg) and seg[j] == "]":
                j += 1
            while j < len(seg) and seg[j] != "]":
                j += 1
            if j >= len(seg):
                out += re.escape("[")
            else:
                body = seg[i + 1 + (1 if neg else 0):j]
                body = body.replace("\\", "\\\\").replace("^", "\\^")
                out += "[" + ("^" if neg else "") + body + "]"
                i = j
        else:
            out += re.escape(c)
        i += 1
    return re.compile("^" + out + "$", re.S)


def match(pattern: str, path: str) -> bool:
    p, t = pattern.split("/"), path.split("/")
    memo: dict = {}

    def go(i: int, j: int) -> bool:
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == len(p):
            res = j == len(t)
        elif p[i] == "**":
            res = any(go(i + 1, k) for k in range(j, len(t) + 1))
        elif j == len(t):
            res = False
        else:
            res = _seg_regex(p[i]).match(t[j]) is not None and go(i + 1, j + 1)
        memo[key] = res
        return res

    return go(0, 0)
