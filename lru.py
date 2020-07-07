from threading import RLock
from typing import Any, List, Optional

from simple_lru import LruCacheInterface, EvictCallback
from simple_lru.lru import LRU


class Cache:

    def __init__(self, size: int, on_evicted: Optional[EvictCallback] = None, lru_class: LruCacheInterface = LRU,
                 lock=RLock):
        self.lru = lru_class(size, on_evicted)
        self._lock = lock()

    def purge(self):
        with self._lock:
            self.lru.purge()

    def add(self, key: Any, value: Any) -> bool:
        with self._lock:
            evicted = self.lru.add(key, value)
        return evicted

    def get(self, key: Any) -> Any:
        with self._lock:
            value = self.lru.get(key)
        return value

    def __len__(self):
        with self._lock:
            length = len(self.lru)
        return length

    def keys(self) -> List[Any]:
        with self._lock:
            keys = self.lru.keys()
        return keys


cache = Cache(5)
cache.add(5, [1, 2, 3, 4, 5])
print(cache.keys())
cache.add(6, 1)
print(cache.keys())

cache.add(11, 8)
print(cache.keys())
cache.add(12, 7)
print(cache.keys())
cache.add(5, 8)
print(cache.keys())
cache.add(11, 8)
print(cache.keys())
cache.add(19, 7)
print(cache.keys())
cache.add(17, 8)
cache.add(18, 7)
print(cache.keys())
cache.add(12, 7)

print(cache.keys())
cache.add(5, 8)
cache.add(21, 7)
print(cache.keys())
