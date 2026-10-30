from collections import OrderedDict
from typing import Any, Callable


class TTLCache:
    def __init__(self, capacity: int, ttl: float, clock: Callable[[], float]) -> None:
        self.capacity, self.ttl, self.clock = capacity, ttl, clock
        self._d: OrderedDict[Any, tuple[Any, float]] = OrderedDict()

    def _purge(self) -> None:
        now = self.clock()
        for k in [k for k, (_, exp) in self._d.items() if now >= exp]:
            del self._d[k]

    def put(self, key: Any, value: Any) -> None:
        self._purge()
        if key in self._d:
            del self._d[key]
        elif len(self._d) >= self.capacity:
            self._d.popitem(last=False)
        self._d[key] = (value, self.clock() + self.ttl)

    def get(self, key: Any, default: Any = None) -> Any:
        self._purge()
        if key not in self._d:
            return default
        self._d.move_to_end(key)
        return self._d[key][0]

    def __len__(self) -> int:
        self._purge()
        return len(self._d)
