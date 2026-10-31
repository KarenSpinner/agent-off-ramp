import re

_PAT = re.compile(r"^([\[(])\s*(-?\d+)\s*,\s*(-?\d+)\s*([\])])$")


def _parse(s: str):
    m = _PAT.match(s.strip())
    if not m:
        raise ValueError(f"bad interval: {s!r}")
    lo_inc, hi_inc = m.group(1) == "[", m.group(4) == "]"
    lo, hi = int(m.group(2)), int(m.group(3))
    if hi < lo or (hi == lo and not (lo_inc and hi_inc)):
        raise ValueError(f"empty interval: {s!r}")
    return lo, lo_inc, hi, hi_inc


def _fmt(lo, lo_inc, hi, hi_inc) -> str:
    return f"{'[' if lo_inc else '('}{lo},{hi}{']' if hi_inc else ')'}"


def merge(intervals: list[str]) -> list[str]:
    items = sorted((_parse(s) for s in intervals), key=lambda t: (t[0], not t[1]))
    out: list[tuple] = []
    for lo, lo_inc, hi, hi_inc in items:
        if out:
            clo, clo_inc, chi, chi_inc = out[-1]
            if lo < chi or (lo == chi and (chi_inc or lo_inc)):
                if hi > chi or (hi == chi and hi_inc):
                    chi, chi_inc = hi, hi_inc
                out[-1] = (clo, clo_inc, chi, chi_inc)
                continue
        out.append((lo, lo_inc, hi, hi_inc))
    return [_fmt(*t) for t in out]
