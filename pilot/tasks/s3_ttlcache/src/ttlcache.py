'''LRU cache with per-entry TTL and an injectable clock.'''
from collections import OrderedDict
from typing import Any, Callable


class TTLCache:
    def __init__(self, capacity: int, ttl: float, clock: Callable[[], float]) -> None:
        raise NotImplementedError

    def put(self, key: Any, value: Any) -> None:
        raise NotImplementedError

    def get(self, key: Any, default: Any = None) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
