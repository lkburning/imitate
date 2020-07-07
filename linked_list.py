from typing import Optional, Any


class Element:
    def __init__(self, data, user_list: Optional['LinkedList']):
        self.data: Any = data
        self.next: Optional['Element'] = None
        self.prev: Optional['Element'] = None
        self.list = user_list

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getNext(self) -> Optional['Element']:
        return self.next

    def getPrev(self) -> Optional['Element']:
        return self.prev

    # def __eq__(self, other: 'Element') -> bool:
    #     if other.data == self.data and other.prev == self.prev \
    #             and self.next == other.next and other.list == self.list:
    #         return True
    #     return False

    @classmethod
    def build_nil_element(cls):
        return cls(None, None)


class LinkedList:

    def __init__(self, root: Optional['Element'], size: int = 0):
        # 默认第一个值应该是空 element
        self.root = root
        self.size = size

    @classmethod
    def build_nil_list(cls):
        element = Element.build_nil_element()
        linked_list = cls(element)
        linked_list.root.next = element
        linked_list.root.next.prev = linked_list.root
        linked_list.root.list = linked_list
        return linked_list

    def insert(self, e: Element, at: Element) -> Element:
        e.prev = at
        e.next = at.next
        e.prev.next = e
        e.next.prev = e
        e.list = self
        self.size += 1
        return e

    def front(self) -> Optional[Element]:
        if self.size == 0:
            return None
        return self.root.next

    def back(self) -> Optional[Element]:
        if self.size == 0:
            return None
        return self.root.prev

    def _remove(self, e: Element) -> Element:
        e.prev.next = e.next
        e.next.prev = e.prev
        e.next = None
        e.prev = None
        self.list = None
        self.size -= 1
        return e

    def insert_value(self, v: Any, at: Element) -> Element:
        e = Element(v, None)
        return self.insert(e, at)

    def move(selfe, e: Element, at: Element) -> Element:
        if e == at:
            return e
        e.prev.next = e.next
        e.next.prev = e.prev

        e.prev = at
        e.next = at.next
        e.prev.next = e
        e.next.prev = e
        return e

    def remove(self, e: Element) -> Any:
        if e.list == self:
            self._remove(e)
        return e.data

    def lazy_init(self) -> 'LinkedList':
        if self.root.next is None:
            element = Element.build_nil_element()
            self.root = element
            self.root.list = self
            self.size = 0
        return self

    def push_back(self, v: Any) -> Element:
        self.lazy_init()
        return self.insert_value(v, self.root.prev)

    def insert_before(self, v: Any, mark: Element) -> Optional[Element]:
        if mark.list != self:
            return None
        return self.insert_value(v, mark.prev)

    def insert_after(self, v: Any, mark: Element) -> Optional[Element]:
        if mark.list != self:
            return None

        return self.insert_value(v, mark)

    def move_to_front(self, e: Element) -> None:
        if e.list != self or self.root.next == e:
            return None
        self.move(e, self.root)

    def move_to_back(self, e: Element) -> None:
        if e.list != self or self.root.prev == e:
            return None
        self.move(e, self.root.prev)

    def move_before(self, e: Element, mark: Element):
        if e.list != self or e == mark or mark.list != self:
            return
        self.move(e, mark)

    def push_back_list(self, other: 'LinkedList'):
        self.lazy_init()
        i, e = other.size, other.front()
        for _ in range(i, 0, -1):
            self.insert_value(e.data, self.root)
            e = e.getNext()

    def push_front_list(self, other: 'LinkedList'):
        self.lazy_init()
        i, e = other.size, other.back()
        for _ in range(i, 0, -1):
            self.insert_value(e.data, self.root)
            e = e.getNext()

    def push_front(self, v: Any) -> Element:
        self.lazy_init()
        return self.insert_value(v, self.root)

    def len(self):
        return self.size

    def __len__(self):
        return self.len()
