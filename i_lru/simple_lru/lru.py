from typing import Any, Dict, Hashable, Tuple, List, Optional

import linked_list
from i_lru.exception import KeyNotFoundError
from . import EvictCallback, LinkedListElement
from . import LruCacheInterface


class Entry:

    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value


class Empty(object):
    pass


empty = Empty()


class LRU(LruCacheInterface):

    def __init__(self, size: int, on_evict: Optional[EvictCallback]):
        super().__init__(size, on_evict)
        self.evict_list: linked_list.LinkedList = linked_list.LinkedList.build_nil_list()
        self.items: Dict[Any, linked_list.Element] = dict()

    def purge(self):
        for key, value in self.items.items():
            if self.on_evict is not None:
                # if not isinstance(value, Entry):
                #     raise TypeError(f"we should get `ENTRY` ,but {type(value)}")
                self.on_evict(key, value)
            self.items.pop(key)
        self.evict_list.build_nil_list()

    def add(self, key: Hashable, value: Any) -> bool:
        ent = self.items.get(key, False)
        if ent:
            self.evict_list.move_to_front(ent)
            return False

        ent = Entry(key, value)
        entry = self.evict_list.push_front(ent)
        self.items[key] = entry

        evict = self.evict_list.len() > self.size

        if evict:
            self.remove_oldest()
        return evict

    def remove_oldest(self) -> Tuple[Any, Any, bool]:
        ent = self.evict_list.back()
        if ent is not None:
            self.remove_element(ent)
        return None, None, False

    def remove_element(self, e: LinkedListElement) -> None:
        self.evict_list.remove(e)
        kv = e.data
        assert isinstance(kv, Entry), f"we should get `Entry`, but {type(kv)}"
        self.items.pop(kv.key)
        if self.on_evict is not None:
            self.on_evict(kv.key, kv.value)

    def __len__(self) -> int:
        return len(self.evict_list)

    def keys(self) -> List[Any]:
        keys = []
        ent = self.evict_list.back()
        while ent.data:
            assert isinstance(ent.data, Entry), f"we should get `Entry`, but {type(ent.data)}"
            keys.append(ent.data.key)
            ent = ent.getPrev()
        return keys

    def get_oldset(self) -> Tuple[Any, Any, bool]:
        ent = self.evict_list.back()
        if ent is not None:
            kv = ent.data
            assert isinstance(kv, Entry), f"we should get `Entry`, but {type(kv)}"
            return kv.key, kv.value, True
        return None, None, False

    def get(self, key: Any) -> Any:

        ent = self.items.get(key, empty)
        if ent is empty:
            raise KeyNotFoundError(f"{key} not found in cache")
        if ent is None:
            raise KeyNotFoundError(f"{key} not found in cache")
        assert isinstance(ent.data, Entry)
        self.evict_list.move_to_front(ent)
        return ent.data.value

    def contains(self, key: Any) -> bool:
        if self.items.get(key, empty) is empty:
            return False
        return True

    def peek(self, key: Any) -> Any:
        ent = self.items.get(key, empty)
        if ent is empty:
            raise KeyNotFoundError(f"{key}")
        assert isinstance(ent.data, Entry)
        return ent.data.value
