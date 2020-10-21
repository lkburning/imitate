import ctypes  # provide a low-level arrays
from typing import Any


class DynamicArray:

    def __init__(self):
        self._n = 0
        self._capacity = 1
        self._low_array = self._make_array(self._capacity)
        self._null = 0

    def _make_array(self, capacity: int):
        """return new array with capacity array"""
        return (capacity * ctypes.py_object)()

    def append(self, obj: Any) -> None:
        """Add object to end of the array"""
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._low_array[self._n] = obj
        self._n += 1

    def _resize(self, capacity: int) -> None:
        tem_array = self._make_array(capacity)
        for i in range(self._n):
            tem_array[i] = self._low_array[i]
        self._low_array = tem_array
        self._capacity = capacity

    def __len__(self) -> int:
        return self._n

    def __getitem__(self, _index: int) -> Any:
        real_index = self._real_index(_index)
        return self._low_array[real_index]

    def _real_index(self, _index: int) -> int:
        if _index >= 0:
            real_index = _index
        else:
            real_index = self._n + _index
        if real_index >= self._n:
            raise IndexError(f"The index ({_index}) transfinite ({self._n})")
        return real_index

    def pop(self, _index: int = -1) -> Any:
        real_index = self._real_index(_index)
        pop_value = self._low_array[real_index]
        for i in range(real_index, self._n - 1):
            self._low_array[i] = self._low_array[i + 1]
        self._low_array[self._n - 1] = 0
        self._n -= 1
        return pop_value

    def __iter__(self) -> Any:
        for i in range(self._n):
            yield self._low_array[i]

    def __repr__(self) -> str:
        show = '['
        for i in range(self._n):
            show += str(self._low_array[i])
            show += ', '
        show += ']'
        return show

    __str__ = __repr__

    def insert(self, _index: int, value: Any) -> None:
        if _index < 0 or _index > self._n:
            raise IndexError(f"Index({_index}) transfinite")
        if self._n + 1 >= self._capacity:
            self._resize(self._capacity * 2)
        if _index == self._n:
            self.append(value)
        for i in range(self._n, _index, -1):
            self._low_array[i] = self._low_array[i - 1]
        self._low_array[_index] = value
        self._n += 1

    def clear(self) -> None:
        self._n = 0
        self._capacity = 1
        self._low_array = self._make_array(self._capacity)

    def index(self, value:Any, _start:int=0, _stop:int=-1) -> int:
        real_start_index = self._real_index(_start)
        real_stop_index = self._real_index(_stop)
        if real_start_index >= real_stop_index:
            raise ValueError(f"Index({_start} ~ {_stop}) scope error!")
        for i in range(real_start_index, real_stop_index+1):
            if value == self._low_array[i]:
                return i
        return -1


if __name__ == '__main__':
    array = DynamicArray()
    array.append(1)
    array.append(2)
    array.append(3)
    array.append(5)
    print(array)
    array.insert(2, 6)
    print(len(array))
    print(array)
    print(array.index(99))
