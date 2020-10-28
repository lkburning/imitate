from aton import atoi, atof, unsigned_str
import pytest


def test_atoi():
    assert atoi('998') == 998
    assert atoi('+998') == 998
    assert atoi('-998') == -998
    with pytest.raises(ValueError):
        atoi('--998')
    with pytest.raises(ValueError):
        atoi('998.234')


def test_unsigned():
    assert 1,'=123' == unsigned_str('=1223')
    assert -1, '123' == unsigned_str('-123')
    assert 1, '123' == unsigned_str('+123')
    with pytest.raises(AssertionError):
        unsigned_str(12)


def test_atof():
    assert atof('998') == 998
    assert atof('+998') == 998
    assert atof('-998') == -998
    assert atof('998.1') == 998.1
    assert atof('+998.1') == 998.1
    assert atof('-998.1') == -998.1
    with pytest.raises(ValueError):
        atoi('--998')
    with pytest.raises(ValueError):
        atoi('998.23.4')