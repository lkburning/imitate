import array
from typing import Hashable, Generator, Any, Iterable, Tuple
from collections import MutableMapping

# 表示该位置上还没有被放上任何值
FREE = -1
# 表示该位置上以前是有值的， 只是后来被用户删除了
DUMMY = -2


class _Empty:
    pass


_empty = _Empty()


class Dict:

    @staticmethod
    def _make_index(n):
        """New sequence of indices using the smallest possible datatype"""
        # 'b' singed char ， 占用一个字节， 表示0 ~ 2 **7 - 1
        if n <= 2 ** 7: return array.array('b', [FREE]) * n
        # 'h' signed short, 占用两个字节 表示 0 ~ 2 ** 15 -1
        if n <= 2 ** 15: return array.array('h', [FREE]) * n
        # 'l' signed long, 占用 4个字节大小， 0 ~ 2 ** 31 -1
        if n <= 2 ** 31: return array.array('l', [FREE]) * n
        # 使用 python 的整数类型
        return [FREE] * n

    def __init__(self):
        self._init()

    def _init(self):
        # 初始化设置长度为 8 位
        self._indices = self._make_index(8)
        self._size = 0
        # used + dummy
        self._filled = 0

        self._hash_list = []
        self._key_list = []
        self._value_list = []

    def clear(self):
        self._init()

    @staticmethod
    def _gen_probes(hash_value: int, mask: int) -> Generator[int, None, None]:
        PERTRRB_SHIFT = 5
        hash_value = abs(hash_value)
        # 111111 & 000001 ==> 1
        i = hash_value & mask
        yield i
        perturb = hash_value
        while True:
            i = (5 * i + perturb + 1) & 0xFFFFFFFFFFFFFFFFF
            yield i & mask
            # 二进制右移 PERTRRB_SHIFT 位
            # 1111 10101 =》 1111
            perturb >>= PERTRRB_SHIFT

    def _look_up(self, key: Hashable, hash_value: int):
        assert self._filled < len(self._indices)
        freeslot = None
        for i in self._gen_probes(hash_value, len(self._indices) - 1):
            index = self._indices[i]
            if index == FREE:
                return (FREE, i) if freeslot is None else (DUMMY, freeslot)
            if index == DUMMY:
                if freeslot is None:
                    freeslot = i
            # and 的优先级是高于 or 的
            elif self._key_list[index] is key or (self._hash_list[index] == hash_value and
                                                  self._key_list[index] == key):
                return (index, i)

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = self.hash(key)
        index, i = self._look_up(key, hash_value)
        if index < 0:
            raise KeyError(f'{key} not founded!')
        return self._value_list[index]

    def hash(self, key: Hashable) -> int:
        return hash(key)

    def __setitem__(self, key: Hashable, value: Any):
        hash_value = self.hash(key)
        index, i = self._look_up(key, hash_value)
        if index < 0:
            self._indices[i] = self._size
            self._hash_list.append(hash_value)
            self._key_list.append(key)
            self._value_list.append(value)
            self._size += 1
            if index == FREE:
                self._filled += 1
                if self._filled * 3 > len(self._indices) * 2:
                    self._resize(4 * len(self))
        else:
            self._value_list[index] = value

    def _resize(self, n: int):
        # n.bit_length 获取二进制下占用的长度
        n = 2 ** n.bit_length()
        print(f"resize: new{n}, old{len(self._indices)}")
        self._indices = self._make_index(n)

        for index, hash_value in enumerate(self._hash_list):
            for i in self._gen_probes(hash_value, n - 1):
                if self._indices[i] == FREE:
                    break
            self._indices[i] = index
        self._filled = self._size

    def __len__(self):
        return self._size

    def __delitem__(self, key: Hashable):
        hash_value = self.hash(key)
        index, i = self._look_up(key, hash_value)
        self._size -= 1
        if index < 0:
            raise KeyError(f'{key} not founded!')
        self._indices[i] = DUMMY
        self._hash_list.pop(index)
        self._key_list.pop(index)
        self._value_list.pop(index)
        for i in range(len(self._indices)):
            if self._indices[i] > index:
                self._indices[i] -= 1
        # 如果已经删除的元素达到了使用中的位置的 1/3
        if (self._filled - self._size) * 3 > self._filled:
            self._resize(4 * min(len(self), 2))

    def pop(self, key: Hashable, default: Any = _empty) -> Any:
        if len(self._key_list) == 0:
            if default is _empty:
                raise KeyError(f"{key} not founded!")
            return default
        try:
            del self[key]
        except KeyError:
            if default is _empty:
                raise
            return default

    def __repr__(self) -> str:
        result = '{'
        result += " , ".join([f"{key} : {value}" for key, value in self.items()])
        return result + ' }'

    __str__ = __repr__

    def keys(self) -> Iterable[Hashable]:
        for key in self._key_list:
            yield key

    def values(self) -> Iterable[Any]:
        for value in self._value_list:
            return value

    def items(self) -> Iterable[Tuple[Hashable, Any]]:
        for i in range(self._size):
            yield self._key_list[i], self._value_list[i]
