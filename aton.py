from array import array
from typing import Tuple


def new_unsigned_short_array() -> array:
    return array('H')


def unsigned_str(value: str) -> Tuple[int, str]:
    assert isinstance(value, str), f"value must str, but {type(value)}"
    first = value[0]
    if first in ('+', '-'):
        signed = 1 if first == '+' else -1
        value = value[1:]
    else:
        signed = 1
    return signed, value


def atoi(value: str) -> int:
    """Converts a string to an integer, if it is a valid string, otherwise raises ValueError"""
    signed, unsigned_value = unsigned_str(value)
    int_array = new_unsigned_short_array()
    for i in unsigned_value:
        diff = ord(i) - ord('0')
        if 0 <= diff <= 9:
            int_array.append(diff)
        else:
            raise ValueError(f'invalid literal for int() with base 10: {i}')
    digits = len(int_array)
    return signed * sum(int_array[i] * (10 ** (digits - i - 1)) for i in range(digits))


def atof(value: str) -> float:
    """Converts a string to an float, if it is a valid string, otherwise raises ValueError"""
    signed, unsigned_value = unsigned_str(value)
    int_array = new_unsigned_short_array()
    decimal = new_unsigned_short_array()
    decimal_point_count = 0
    for i in unsigned_value:
        diff = ord(i) - ord('0')
        if i == ".":
            if decimal_point_count:
                raise ValueError(f"could not convert string to float: '{value}'")
            decimal_point_count += 1
            continue

        if not( 0 <= diff <= 9):
            raise ValueError(f"could not convert string to float: '{value}'")

        if decimal_point_count:
            decimal.append(diff)
        else:
            int_array.append(diff)
    int_digits, decimal_digits = len(int_array), len(decimal)
    return float(signed * (sum(int_array[i] * (10 ** (int_digits - i - 1)) for i in range(int_digits)) +
                     sum(decimal[i] * 10 ** (-1 * (i + 1)) for i in range(decimal_digits))))
