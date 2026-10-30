from datetime import datetime, timedelta


def _field(tok: str, lo: int, hi: int):
    if tok == "*":
        return None
    if not tok.isdigit():
        raise ValueError(f"bad field {tok!r}")
    v = int(tok)
    if not lo <= v <= hi:
        raise ValueError(f"out of range {tok!r}")
    return v


def next_run(spec: str, after: datetime) -> datetime:
    parts = spec.split()
    if len(parts) != 3:
        raise ValueError("spec must have exactly three fields")
    minute, hour, dom = _field(parts[0], 0, 59), _field(parts[1], 0, 23), _field(parts[2], 1, 31)
    t = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
    day = t.replace(hour=0, minute=0)
    for _ in range(366 * 9):
        if dom is None or day.day == dom:
            for h in ([hour] if hour is not None else range(24)):
                for m in ([minute] if minute is not None else range(60)):
                    cand = day.replace(hour=h, minute=m)
                    if cand >= t:
                        return cand
        day += timedelta(days=1)
    raise ValueError("no matching time")
