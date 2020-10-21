from typing import Callable, NewType, Any, Hashable, Tuple, List, Optional

import linked_list

EvictCallback = NewType('EvictCallback', Callable[[Any, Any], None])
LinkedListType = NewType('LinkedListType', linked_list.LinkedList)
LinkedListElement = NewType('LinkedListElement', linked_list.Element)


class LruCacheInterface:

    def __init__(self, size: int, on_evict: Optional[EvictCallback]):
        self.size = size
        self.on_evict = on_evict

    def purge(self) -> None:
        raise NotImplementedError

    def add(self, key: Hashable, value: Any) -> bool:
        raise NotImplementedError

    def remove_oldest(self) -> Tuple[Any, Any, bool]:
        raise NotImplementedError

    def remove_element(self, e: LinkedListElement):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def keys(self) -> List[Any]:
        raise NotImplementedError

    def get_oldset(self) -> Tuple[Any, Any, bool]:
        raise NotImplementedError

    def get(self, key: Any) -> Any:
        raise NotImplementedError

    def contains(self, key: Any) -> bool:
        raise NotImplementedError

    def peek(self, key: Any) -> Any:
        raise NotImplementedError
