from src.ttlcache import TTLCache


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def test_replace_does_not_evict():
    c = Clock()
    cache = TTLCache(2, 100, c)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 3)
    assert cache.get("b") == 2 and cache.get("a") == 3 and len(cache) == 2


def test_capacity_one():
    c = Clock()
    cache = TTLCache(1, 100, c)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") is None and cache.get("b") == 2
