from typing import Any, Optional


class EmptyError(Exception):
    pass


class _Node:
    __slots__ = '_element', '_prev', '_next'

    def __init__(self, element: Any, prev: Optional['_Node'], next: Optional['_Node']):
        self._element = element
        self._prev = prev
        self._next = next

    def element(self) -> Any:
        return self._element

    def __repr__(self):
        return f'{self._element}(p)'

    __str__ = __repr__


class _DoublyLinkedListBase:

    def __init__(self):
        self._header = _Node(None, None, None)
        self._trailer = _Node(None, None, None)
        self._header._next = self._trailer
        self._header._prev = self._header
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _insert_between(self, e: Any, predecessor: _Node, successor: _Node):
        newest_node = _Node(e, predecessor, successor)
        predecessor._next = newest_node
        successor._prev = newest_node
        self._size += 1
        return newest_node

    def _delete_node(self, node: _Node) -> _Node:
        predecessor = node._prev
        successor = node._next

        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        del node
        return element

    def __repr__(self):
        if self.is_empty():
            return ""
        elements = []
        ele = self._header._next
        while not (ele is self._trailer):
            elements.append(str(ele._element))
            ele = ele._next
        return ' <-> '.join(elements)

    __str__ = __repr__


class LinkedDeque(_DoublyLinkedListBase):

    def first(self) -> Any:
        if self.is_empty():
            raise EmptyError("Deque is empty")
        return self._header._next._element

    def last(self) -> Any:
        if self.is_empty():
            raise EmptyError("Deque is empty")
        return self._trailer._prev._element

    def insert_first(self, e: Any):
        self._insert_between(e, self._header, self._header._next)

    def inner_last(self, e: Any):
        self._insert_between(e, self._trailer._prev, self._trailer)

    def delete_first(self) -> Any:
        if self.is_empty():
            raise EmptyError("Deque is empty!")
        return self._delete_node(self._header._next)

    def delete_last(self) -> Any:
        if self.is_empty():
            raise EmptyError("Deque is empty!")
        return self._delete_node(self._trailer._prev)

    def __iter__(self):
        if self.is_empty():
            raise StopIteration('Empty Position List')
        ele = self._header._next
        while not (ele is self._trailer):
            yield ele
            ele = ele._next


class PositionList(_DoublyLinkedListBase):

    def first(self) -> Optional['_Node']:
        if self.is_empty():
            return None
        return self._header._next

    def last(self) -> Optional['_Node']:
        if self.is_empty():
            return None
        return self._trailer._prev

    def before(self, p:_Node) -> Optional[_Node]:
        if self._header is p._prev:
            return None
        return p._prev

    def after(self, p:_Node) -> Optional[_Node]:
        if self._trailer is p._next:
            return None
        return p._next

    def __iter__(self):
        if self.is_empty():
            raise StopIteration('Empty Position List')
        ele = self._header._next
        while not (ele is self._trailer):
            yield ele
            ele = ele._next

    def add_first(self, e:Any) -> '_Node':
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e:Any) -> '_Node':
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p:_Node, e:Any) -> '_Node':
        return self._insert_between(e, p._prev, p)

    def add_after(self, p:_Node, e:Any) -> '_Node':
        return self._insert_between(e, p, p._next)

    def replace(self, p:_Node, e:Any)-> Any:
        ele = p.element()
        p._element = e
        return ele

    def delete(self, e:_Node) -> Any:
        return self._delete_node(e)







if __name__ == '__main__':
    deque = LinkedDeque()
    deque.insert_first(5)
    deque.insert_first(4)
    deque.insert_first(3)
    deque.inner_last(2)
    deque.inner_last(11)
    print(deque)
    for i in deque:
        print(i)
    de = iter(deque)

