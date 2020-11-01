from abc import abstractmethod
from typing import Any, Optional, List, Callable, runtime_checkable, Protocol, Union


@runtime_checkable
class SupportsGt(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()

    @abstractmethod
    def __gt__(self, other) -> bool:
        pass


@runtime_checkable
class SupportsLt(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass


@runtime_checkable
class SupportsGe(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()

    @abstractmethod
    def __ge__(self, other) -> bool:
        pass


@runtime_checkable
class SupportsLe(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()

    @abstractmethod
    def __le__(self, other) -> bool:
        pass


SupportsCompare = Union[SupportsGe, SupportsGt, SupportsLe, SupportsLt]


class EmptyError(Exception):
    pass


class SizeLimitError(Exception):
    pass


class _Node:
    __slots__ = 'element', 'next_node'

    def __init__(self, element: Any, next_node: Optional['_Node']):
        self.element = element
        self.next_node = next_node

    def __repr__(self):
        return str(self.element)

    __str__ = __repr__


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


class LinkedList:

    def __init__(self):
        self._head: Optional['_Node'] = None
        self._tail: Optional['_Node'] = None
        self._size: int = 0

    def __repr__(self):
        if not self._size:
            return ''
        elements = []
        node = self._head
        while node:
            elements.append(str(node.element))
            node = node.next_node
        return ' -> '.join(elements)

    __str__ = __repr__

    def append(self, e: Any):
        node = _Node(e, None)
        if self._size == 0:
            self._head = node
        else:
            self._tail.next_node = node
        self._tail = node
        self._size += 1

    def push(self, e: Any) -> None:
        node = _Node(e, None)
        if self._size == 0:
            self._tail = node
        else:
            node.next_node = self._head
        self._head = node
        self._size += 1

    def exist(self, e: Any) -> bool:
        if not self._size:
            return False
        node = self._head
        while node:
            if node.element == e:
                return True
            node = node.next_node
        return False

    def sort(self, key: Callable[[Any], SupportsCompare] = None, reverse: bool = True) -> None:
        if key is None:
            key = lambda x: x
        if self._size <= 1:
            return

        i = 0
        while i < self._size - 1:
            prev = None
            current = self._head
            j = 0
            while j < self._size - 1 - i:
                if not current.next_node:
                    break
                next = current.next_node
                if (reverse and (key(current.element) < key(next.element))) or (
                        (not reverse) and (key(current.element) > key(next.element))):
                    if j == 0:
                        self._head = next
                    else:
                        prev.next_node = next
                    current.next_node = next.next_node
                    prev = next
                    next.next_node = current
                else:
                    prev = current
                    current = next
                j += 1

            if i == 0:
                self._tail = current
            i += 1

    def __len__(self):
        return self._size

    def insert(self, e: Any, position=0):
        if position == self._size:
            self.append(e)
        elif position == 0:
            self.push(e)
        else:
            real_position = self.real_position(position)
            node = _Node(e, None)
            tem = self._head
            index = 0
            while True:
                if index == real_position:
                    old_current_node = tem.next_node
                    tem.next_node = node
                    node.next_node = old_current_node
                    break
                index += 1
            self._size += 1

    def pop(self, position=0):
        position = self.real_position(position)
        tem = self._head
        if self._size == 1:
            self._tail = self._head = None
        elif position == 0:
            self._head = tem.next_node
        else:
            index = 0
            while True:
                index += 1
                if index == position:
                    current_node = tem.next_node
                    tem.next_node = current_node.next_node
                    if tem.next_node == None:
                        self._tail = tem
                    break
                tem = tem.next_node

        self._size -= 1

    def real_position(self, position: int) -> int:
        assert isinstance(position, int)
        if position < 0:
            result = self._size + position
        else:
            result = position
        if 0 <= result < self._size:
            return result
        raise IndexError("Index illegal!")

    def __getitem__(self, position: int) -> Any:
        return self.get_position_node(position).element

    def get_position_node(self, position: int) -> '_Node':
        real_position = self.real_position(position)
        start = 0
        node = self._head

        while start < real_position:
            node = node.next_node
            start += 1
        return node

    def rotate_right(self, k: int):
        rotate_number = self._rotate_number(k)
        # 第一种代码
        # for _ in range(rotate_number):
        #     self._rotate_right()

        # 第二种代码
        if not (rotate_number and self._size > 1):
            return
            # 找到需要被移动的节点
        tem = self._head
        index = 0
        while True:
            if index == (self._size - rotate_number - 1):
                new_head = tem.next_node
                tem.next_node = None
                self._tail = tem
                break
            index += 1
            tem = tem.next_node
        old_head = self._head
        self._head = old_head_last = new_head
        while old_head_last.next_node:
            old_head_last = old_head_last.next_node
        old_head_last.next_node = old_head

    def _rotate_number(self, k: int) -> int:
        assert isinstance(k, int) and k >= 0
        if self._size == 0:
            return 0
        return k % self._size

    def _rotate_right(self):
        if self._size <= 1:
            return

        # 最后一个node 成了 新的第一个节点
        old_head = self._head
        self._head = self._tail
        self._tail.next_node = old_head

        # 更新新的 tail
        index = 0
        while True:
            if index == self._size - 2:
                old_head.next_node = None
                self._tail = old_head
                break
            old_head = old_head.next_node
            index += 1

    def rotate_left(self, k: int):
        for _ in range(self._rotate_number(k)):
            self._rotate_left()

    def _rotate_left(self):
        if self._size <= 1:
            return
        old_head = self._head
        self._head = old_head.next_node
        old_head.next_node = None
        self._tail.next_node = old_head
        self._tail = old_head

    def reverse(self) -> 'LinkedList':
        new_linked_list = LinkedList()
        head = self._head
        while head:
            new_linked_list.insert(head.element)
            head = head.next_node
        return new_linked_list

    def __add__(self, other: 'LinkedList') -> 'LinkedList':
        """
        Leetcode 445. 两数相加 II
        """
        short = other.reverse() if len(self) >= len(other) else self.reverse()
        long = other.reverse() if len(self) < len(other) else self.reverse()
        result = LinkedList()
        start, stop = 0, max(len(short), len(long))
        carry, current = 0, 0
        short_node, long_node = short._head, long._head
        while start < stop:
            if start < len(short):
                current = long_node.element + short_node.element + carry
                short_node = short_node.next_node
            else:
                current = long_node.element +carry
            carry = int(current / 10)
            current = current % 10
            long_node = long_node.next_node
            start += 1
            result.insert(current)
        if carry == 1:
            result.insert(1)
        return result


if __name__ == '__main__':
    # c = SinglyLinkedStack()
    # c.push(5)
    # c.push(6)
    # c.push(7)
    # print('Linked Stack:', c)
    # c.top()
    # c.pop()
    # print('Linked Stack:', c)
    # d = SinglyLinkedQueue(3)
    # d.enqueue(4)
    # d.enqueue(5)
    # d.enqueue(6)
    # print('Linked Queue:', d)
    # try:
    #     d.enqueue(7)
    # except SizeLimitError:
    #     pass
    # d.dequeue()
    # print('Linked Queue:', d)
    #
    # f = CircularQueue(3)
    # f.enqueue(1)
    # f.enqueue(2)
    # f.enqueue(3)
    # print('Circular Queue:', f)
    # try:
    #     f.enqueue(4)
    # except SizeLimitError:
    #     pass
    # f.dequeue()
    # print('Circular Queue:', f)
    # f.enqueue(4)
    # print('Circular Queue:', f)
    # f.rotate()
    # print('Circular Queue:', f)
    # f.dequeue()
    # f.dequeue()
    # print('Circular Queue:', f)
    f = LinkedList()
    f.append(7)
    f.append(2)
    f.append(4)
    f.append(3)
    # f.append(9)
    # f.push(32)
    print(f)
    e = LinkedList()
    e.append(5)
    e.append(6)
    e.append(4)
    print(e)
    print(f +e)
    # f.rotate_left(1)
    # print(f)
    # f.rotate_left(1)
    # print(f)
    # f.rotate_left(1)
    # print(f)
    # f.rotate_left(13)
    # f.reverse()
    # print(f)

    # f.sort()
    # print(f)
    # f.pop(2)
    # print(f)
    # f.insert(2, 2)
    # print(f)
