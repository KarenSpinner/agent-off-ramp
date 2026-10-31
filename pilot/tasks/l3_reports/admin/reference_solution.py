def merge(primary: list[dict], secondary: list[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    for recs in (primary, secondary):
        for r in recs:
            if r["id"] not in seen:
                seen[r["id"]] = dict(r)
    return sorted(seen.values(), key=lambda r: (r["date"], r["id"]))
