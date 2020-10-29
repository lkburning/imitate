from typing import Any, Optional, List


class EmptyError(Exception):
    pass


class SizeLimitError(Exception):
    pass


class _Node:
    __slots__ = 'element', 'next_node'

    def __init__(self, element: Any, next_node: Optional['_Node']):
        self.element = element
        self.next_node = next_node


class SinglyLinkedStack:

    def __init__(self):
        self._head: Optional['_Node'] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return not bool(self._size)

    def push(self, e: Any):
        """Add a element to the top of the stack"""
        self._head = _Node(e, self._head)
        self._size += 1

    def top(self) -> Any:
        """
        Return (but not remove) the element at the top of the stack

        :raise EmptyError
        """
        if self.is_empty():
            raise EmptyError('LinkedList is Empty')
        return self._head.element

    def pop(self) -> Any:
        """
        Remove and return the element form the top of the stack

        :raise EmptyError
        """
        if self.is_empty():
            raise EmptyError('LinkedList is Empty')
        result = self._head
        self._head = result.next_node
        self._size -= 1
        return result.element

    def __repr__(self) -> str:
        if self.is_empty():
            return ''
        elements: List[str] = []
        tmp = self._head
        while tmp:
            elements.append(str(tmp.element))
            tmp = tmp.next_node
        return ' -> '.join(elements)

    __str__ = __repr__


class SinglyLinkedQueue:

    def __init__(self, max_size: int):
        assert isinstance(max_size, int) and max_size > 0, 'Queue size must is int and gt 0'
        self.max_size = max_size
        self._head = None
        self._size = 0
        self._tail = None

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return not bool(self._size)

    def first(self) -> Any:
        if self.is_empty():
            raise EmptyError('Queue is Empty')
        return self._head.element

    def enqueue(self, e: Any):
        if self._size > self.max_size - 1:
            raise SizeLimitError(f'Exceeding the maximum size({self.max_size}) limit')
        node = _Node(e, None)
        if self.is_empty():
            self._head = node
        else:
            self._tail.next_node = node
        self._tail = node
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise EmptyError('Queue is empty!')
        result = self._head
        self._head = result.next_node
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return result.element

    def __repr__(self) -> str:
        if self.is_empty():
            return ''

        elements: List[str] = []
        tmp = self._head
        while tmp:
            elements.append(str(tmp.element))
            tmp = tmp.next_node
        return ' -> '.join(elements)

    __str__ = __repr__


class CircularQueue:

    def __init__(self, max_size: int):
        assert isinstance(max_size, int) and max_size > 0, 'Queue size must is int and gt 0'
        self._tail = None
        self._size = 0
        self.max_size = max_size

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return not bool(self._size)

    def first(self) -> Any:
        if self.is_empty():
            raise EmptyError('Queue is empty!')
        return self._tail.next_node.element

    def enqueue(self, e: Any):
        if self._size > self.max_size - 1:
            raise SizeLimitError(f'Exceeding the maximum size({self.max_size}) limit')
        node = _Node(e, None)
        if self.is_empty():
            # node.next_node = node
            self._tail = node
            head = node
        else:
            # node.next_node = self._tail.next_node
            # self._tail.next_node = node
            head = self._tail.next_node
            self._tail.next_node = node
            self._tail = node
        self._tail.next_node = head
        # self._tail = node
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise EmptyError('Queue is Empty')
        head = self._tail.next_node
        if self._size == 1:
            self._tail = None
        self._tail.next_node = head.next_node
        self._size -= 1
        return head.element

    def rotate(self):
        if not self.is_empty():
            self._tail = self._tail.next_node

    def __repr__(self) -> str:
        if self.is_empty():
            return ''
        elements: List[str] = []
        tmp = self._tail.next_node
        tail = self._tail
        while not (tmp is tail):
            elements.append(str(tmp.element))
            tmp = tmp.next_node
        elements.append(str(tmp.element))
        return ' -> '.join(elements)

    __str__ = __repr__


if __name__ == '__main__':
    c = SinglyLinkedStack()
    c.push(5)
    c.push(6)
    c.push(7)
    print('Linked Stack:', c)
    c.top()
    c.pop()
    print('Linked Stack:', c)
    d = SinglyLinkedQueue(3)
    d.enqueue(4)
    d.enqueue(5)
    d.enqueue(6)
    print('Linked Queue:', d)
    try:
        d.enqueue(7)
    except SizeLimitError:
        pass
    d.dequeue()
    print('Linked Queue:', d)

    f = CircularQueue(3)
    f.enqueue(1)
    f.enqueue(2)
    f.enqueue(3)
    print('Circular Queue:', f)
    try:
        f.enqueue(4)
    except SizeLimitError:
        pass
    f.dequeue()
    print('Circular Queue:', f)
    f.enqueue(4)
    print('Circular Queue:', f)
    f.rotate()
    print('Circular Queue:', f)
    f.dequeue()
    f.dequeue()
    print('Circular Queue:', f)
