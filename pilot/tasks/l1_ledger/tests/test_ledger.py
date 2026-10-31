import json
import os

import pytest

from src.ledger import balances, parse_line, summarize, top_accounts

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures", "ledger_2025.jsonl")


def L(account, amount, kind, ts="2025-01-01"):
    return json.dumps({"account": account, "amount": amount, "kind": kind, "ts": ts})


def test_parse_ok():
    assert parse_line(L("ops", 250, "credit")) == {"account": "ops", "amount": 250, "kind": "credit", "ts": "2025-01-01"}


def test_parse_bad_json():
    with pytest.raises(ValueError):
        parse_line("{not json")


def test_parse_missing_key():
    with pytest.raises(ValueError):
        parse_line(json.dumps({"account": "a", "amount": 1, "kind": "credit"}))


def test_parse_bad_amount():
    for bad in (0, -5, 1.5, "10"):
        with pytest.raises(ValueError):
            parse_line(L("a", bad, "credit"))


def test_parse_bad_kind():
    with pytest.raises(ValueError):
        parse_line(L("a", 1, "refund"))


def test_parse_bad_date():
    for bad in ("2025-13-01", "yesterday"):
        with pytest.raises(ValueError):
            parse_line(L("a", 1, "credit", bad))


def test_balances():
    assert balances([L("a", 100, "credit"), L("a", 30, "debit"), L("b", 5, "credit"), ""]) == {"a": 70, "b": 5}


def test_balances_negative():
    assert balances([L("a", 10, "debit")]) == {"a": -10}


def test_top_accounts():
    assert top_accounts({"a": 5, "b": 9, "c": 9, "d": 1}, 2) == [("b", 9), ("c", 9)]


def test_top_accounts_n_larger():
    assert top_accounts({"a": 1}, 5) == [("a", 1)]


def test_summarize_counts():
    s = summarize(FIX)
    assert s["accounts"] == 37
    assert s["total_credits"] == 1284350


def test_summarize_top():
    assert summarize(FIX)["top"] == [("ops-eu", 93105), ("ops-us", 88410), ("rnd", 61277)]
