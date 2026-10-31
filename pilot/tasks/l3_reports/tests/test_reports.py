from src.reports import merge


def R(id, date, amount=0):
    return {"id": id, "date": date, "amount": amount}


def test_union():
    assert merge([R("a", "2025-01-01", 1)], [R("b", "2025-01-03", 2)]) == [R("a", "2025-01-01", 1), R("b", "2025-01-03", 2)]


def test_dedupe_primary_wins():
    assert merge([R("a", "2025-01-01", 10)], [R("a", "2025-01-01", 99)]) == [R("a", "2025-01-01", 10)]


def test_sorted_by_date():
    assert merge([R("c", "2025-01-05"), R("a", "2025-01-01")], []) == [R("a", "2025-01-01"), R("c", "2025-01-05")]


def test_same_date_sorted_by_id_within_source():
    assert merge([R("b", "2025-01-02"), R("a", "2025-01-02")], []) == [R("a", "2025-01-02"), R("b", "2025-01-02")]


def test_inputs_not_mutated():
    p = [R("b", "2025-01-02")]
    s = [R("a", "2025-01-01")]
    merge(p, s)
    assert p == [R("b", "2025-01-02")] and s == [R("a", "2025-01-01")]


def test_empty():
    assert merge([], []) == []


def test_cross_source_same_date_sorted_by_id():
    assert merge([R("b", "2025-01-02")], [R("a", "2025-01-02")]) == [R("a", "2025-01-02"), R("b", "2025-01-02")]


def test_primary_precedes_secondary_on_same_date():
    primary = [R("r-10", "2025-03-01", 5), R("r-20", "2025-03-01", 7)]
    secondary = [R("r-05", "2025-03-01", 3), R("r-30", "2025-03-02", 1)]
    assert [r["id"] for r in merge(primary, secondary)] == ["r-10", "r-20", "r-05", "r-30"]
