import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from dynamic_array import DynamicArray


class TestDynamicArray:

    def test_append(self):
        array = DynamicArray()
        array.append(2)
        array.append(3)
        assert 2 in array

    def test_index(self):
        array = DynamicArray()
        array.append(1)
        assert array[0] == 1
        with pytest.raises(IndexError):
            _ = array[1]

    def test_slice(self):
        array = DynamicArray()
        array.append(1)
        array.append(2)
        array.append(3)
        test_slice = array[:2]
        assert len(test_slice) == 2
        assert test_slice[0] == 1
        assert test_slice[1] == 2
        with pytest.raises(IndexError):
            _ = array[1:5:1]
        with pytest.raises(IndexError):
            _ = array[5:1]

    def test_insert(self):
        array = DynamicArray()
        array.append(1)
        array.append(2)
        array.insert(1, 3)
        assert array[1] == 3
        with pytest.raises(IndexError):
            array.insert(4, 4)
        assert len(array) == 3

    def test_pop(self):
        array = DynamicArray()
        array.append(1)
        array.append(2)
        array.append(3)
        assert 3 in array
        res = array.pop()
        assert res == 3 and 3 not in array
        assert len(array) == 2
        res_1 = array.pop(0)
        assert res_1 == 1 and 1 not in array
        assert len(array) == 1
        with pytest.raises(IndexError):
            array.pop(3)

    def test_iter(self):
        array = DynamicArray()
        test_data = [1, 2, 3]
        array.append(test_data[0])
        array.append(test_data[1])
        array.append(test_data[2])

        start = 0
        for i in array:
            assert i == test_data[start]
            start += 1

    def test_repr(self):
        array = DynamicArray()
        array.append(1)
        array.append(2)
        assert repr(array) == '[1, 2, ]'
        assert str(array) == '[1, 2, ]'

    def test_remove(self):
        array = DynamicArray()
        array.append(1)
        array.append(2)
        array.remove(2)
        assert 2 not in array and len(array) == 1
        array.append(3)
        array.append(3)
        array.remove(3)
        assert 3 in array and len(array) == 2
        for i in range(100):
            array.append(4)
        for i in range(100):
            array.remove(4)
        assert 4 not in array and len(array) == 2
        assert array._capacity == 8

    def test_count(self):
        array = DynamicArray()
        array.append(1)
        array.append(2)
        array.append(2)
        assert array.count(1) == 1
        assert array.count(2) == 2
        assert array.count(3) == 0

    def test_reverse(self):
        array = DynamicArray()
        test_data = [1, 2, 3]
        array.append(test_data[0])
        array.append(test_data[1])
        array.append(test_data[2])
        array.reverse()

        start = 2
        for i in array:
            assert i == test_data[start]
            start -= 1

    def test_bool(self):
        array = DynamicArray()
        assert bool(array) is False
        array.append(1)
        assert bool(array) is True

    def test_eq(self):
        array, array1 = DynamicArray(), DynamicArray()
        array.append(1)
        assert array != array1
        array1.append(1)
        assert array == array1
        array.append(2)
        array.append(2)
        assert array != array1
        assert [1, 2, 2] != array
