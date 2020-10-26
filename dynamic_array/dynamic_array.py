import ctypes  # provide a low-level arrays
from collections import abc
from math import ceil
from typing import Any, Union, Iterable, Tuple


class DynamicArray:

    def __init__(self, _capacity: int = 1):
        self._n = 0
        assert isinstance(_capacity, int) and _capacity >= 1, "_capacity must int and gt 0"
        self._capacity = _capacity
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

    def __getitem__(self, _index: Union[int, slice]) -> Union[Any, 'DynamicArray']:
        if isinstance(_index, int):
            real_index = self._real_index(_index)
            return self._low_array[real_index]

        elif isinstance(_index, slice):
            start, stop, step = self._slice_params(_index)
            result = DynamicArray(ceil((stop - start) / step))
            for i in range(start, stop, step):
                result.append(self[i])
            return result

        raise ValueError(f'Invalid Index')

    def _slice_params(self, _slice: slice) -> Tuple[int, int, int]:
        start = 0 if _slice.start is None else self._real_index(_slice.start)
        step = 1 if _slice.step is None else _slice.step
        stop = self._n if _slice.stop == self._n or _slice.stop is None else self._real_index(_slice.stop)
        if (start < stop and step > 0) or (start > stop and step < 0):
            return start, stop, step
        raise ValueError(f'Invalid Slice')

    def _real_index(self, _index: int) -> int:
        if _index >= 0:
            real_index = _index
        else:
            real_index = self._n + _index
        if real_index >= self._n:
            raise IndexError(f"The index ({_index}) transfinite ({self._n - 1})")
        return real_index

    def pop(self, _index: int = -1) -> Any:
        real_index = self._real_index(_index)
        pop_value = self._low_array[real_index]
        for i in range(real_index, self._n - 1):
            self._low_array[i] = self._low_array[i + 1]
        self._low_array[self._n - 1] = 0
        self._n -= 1
        self._cut_capacity()
        return pop_value

    def _cut_capacity(self):
        if self._n * 4 < self._capacity:
            self._resize(ceil(self._capacity / 4))

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

    def index(self, value: Any, _start: int = 0, _stop: int = -1) -> int:
        real_start_index = self._real_index(_start)
        real_stop_index = self._real_index(_stop)
        if real_start_index > real_stop_index:
            raise ValueError(f"Index({_start} ~ {_stop}) scope error!")
        for i in range(real_start_index, real_stop_index + 1):
            if value == self._low_array[i]:
                return i
        return -1

    def remove(self, value: Any) -> None:
        """
        Remove first occurrence of value.

        Raises ValueError if the value is not present.
        """
        first_position = self.index(value)
        if first_position == -1:
            raise ValueError(f"{value} not found in array!")
        self.pop(first_position)

    def count(self, value: Any) -> int:
        start, end = 0, self._n
        count = 0
        while start < end:
            first_index = self.index(value, start)
            if first_index == -1:
                break
            else:
                start = first_index + 1
                count += 1
        return count

    def __delitem__(self, key: Union[int, slice]):
        if isinstance(key, int):
            self.pop(key)
        elif isinstance(key, slice):
            start, stop, step = self._slice_params(key)
            for i in range(start, stop, step):
                self.pop(i)

    def reverse(self):
        """ Reverse *IN PLACE*. """
        if self._n <= 1:
            return
        stop = int(self._n / 2)
        for i in range(0, stop):
            temp_current = self._low_array[i]
            swap_index = self._n - 1 - i
            self._low_array[i] = self._low_array[swap_index]
            self._low_array[swap_index] = temp_current
        del temp_current

    def __bool__(self):
        if self._n == 0:
            return False
        return True

    def __add__(self, other: Iterable[Any]):
        if not isinstance(other, abc.Iterable):
            raise TypeError(f"other can not iterable")
        for i in other:
            self.append(i)

    def __eq__(self, other: 'DynamicArray') -> bool:
        if not isinstance(other, DynamicArray):
            return False
        if self._n != other._n:
            return False
        for i in range(0, self._n):
            if self[i] != other[i]:
                return False
        return True

    def __contains__(self, item: Any) -> bool:
        if self.index(item) != -1:
            return True
        return False

    def __gt__(self, other: 'DynamicArray') -> bool:
        min_length = min(self._n, other._n)
        for i in range(min_length):
            if self[i] > other[i]:
                return True
            elif self[i] < other[j]:
                return False
        return True if self._n > other._n else False

    def __lt__(self, other: 'DynamicArray') -> bool:
        if self == other:
            return False
        return not self > other

    def __le__(self, other: 'DynamicArray') -> bool:
        return self < other or self == other

    def __ge__(self, other: 'DynamicArray') -> bool:
        return self > other or self == other

    def __ne__(self, other: 'DynamicArray') -> bool:
        return not self == other
