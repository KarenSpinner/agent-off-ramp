import json
from datetime import date
from typing import Iterable


def parse_line(line: str) -> dict:
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as e:
        raise ValueError(f"bad json: {e}") from None
    if not isinstance(obj, dict) or not {"account", "amount", "kind", "ts"} <= set(obj):
        raise ValueError("missing keys")
    amt = obj["amount"]
    if isinstance(amt, bool) or not isinstance(amt, int) or amt <= 0:
        raise ValueError("bad amount")
    if obj["kind"] not in ("credit", "debit"):
        raise ValueError("bad kind")
    try:
        date.fromisoformat(obj["ts"])
    except (TypeError, ValueError):
        raise ValueError("bad date") from None
    return {"account": obj["account"], "amount": amt, "kind": obj["kind"], "ts": obj["ts"]}


def balances(lines: Iterable[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for line in lines:
        if not line.strip():
            continue
        r = parse_line(line)
        out[r["account"]] = out.get(r["account"], 0) + (r["amount"] if r["kind"] == "credit" else -r["amount"])
    return out


def top_accounts(bal: dict[str, int], n: int) -> list[tuple[str, int]]:
    return sorted(bal.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def summarize(path: str) -> dict:
    with open(path) as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    recs = [parse_line(l) for l in lines]
    bal = balances(lines)
    return {
        "accounts": len(bal),
        "total_credits": sum(r["amount"] for r in recs if r["kind"] == "credit"),
        "top": top_accounts(bal, 3),
    }
