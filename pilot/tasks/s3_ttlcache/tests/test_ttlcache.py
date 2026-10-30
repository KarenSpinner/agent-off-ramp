from src.ttlcache import TTLCache


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def test_basic_put_get():
    c = Clock()
    cache = TTLCache(2, 10, c)
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("zzz", 42) == 42
    assert len(cache) == 1


def test_expiry():
    c = Clock()
    cache = TTLCache(2, 10, c)
    cache.put("a", 1)
    c.t = 9.99
    assert cache.get("a") == 1
    c.t = 10.0
    assert cache.get("a") is None
    assert len(cache) == 0


def test_put_resets_expiry():
    c = Clock()
    cache = TTLCache(2, 10, c)
    cache.put("a", 1)
    c.t = 8
    cache.put("a", 2)
    c.t = 15
    assert cache.get("a") == 2


def test_lru_eviction_counts_get_as_use():
    c = Clock()
    cache = TTLCache(2, 100, c)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_expired_entries_free_capacity():
    c = Clock()
    cache = TTLCache(2, 10, c)
    cache.put("a", 1)
    c.t = 5
    cache.put("b", 2)
    c.t = 10
    cache.put("c", 3)
    assert cache.get("b") == 2
    assert cache.get("c") == 3
    assert len(cache) == 2
