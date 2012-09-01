import sys
import pytest
import _gmpy

class TestInit(object):
    small_ints = {-1, 0, 1, 123, -9876, sys.maxint, -sys.maxint - 1}
    big_ints = {sys.maxint + 1, -sys.maxint - 2, 2 * sys.maxint + 1, 2 * sys.maxint + 2}

    @pytest.mark.parametrize('n', small_ints.union(big_ints))
    def test_init_int(self, n):
        assert _gmpy.mpz(n) == n

    @pytest.mark.parametrize('f', {0.0, 1.0, 1.5, 1e15 + 0.9})
    def test_init_float(self, f):
        assert _gmpy.mpz(f) == int(f)
        assert _gmpy.mpz(-f) == int(-f)

    @pytest.mark.parametrize('n', small_ints.union(big_ints))
    def test_init_decimal_str(self, n):
        assert _gmpy.mpz(str(n), 10) == n
        assert _gmpy.mpz(str(n)) == n
        assert _gmpy.mpz(str(n), 0) == n

    @pytest.mark.parametrize('n', small_ints.union(big_ints))
    def test_init_hex_str(self, n):
        assert _gmpy.mpz("%x" % n, 16) == n
        assert _gmpy.mpz("%#x" % n, 0) == n

    @pytest.mark.parametrize(('n', 'base'), {('0x1', 16), ('g', 16), ('a', 10)})
    def test_init_invalid_str(self, n, base):
        with pytest.raises(ValueError):
            _gmpy.mpz(n, base)

    @pytest.mark.parametrize('type_', {int, float, _gmpy.mpz, str})
    def test_init_type(self, type_):
        assert _gmpy.mpz(type_(1)) == 1


class TestMath(object):
    numbers = {-1, 0, 1, sys.maxint, -sys.maxint - 1, 2 * sys.maxint + 1, 2 * sys.maxint + 2}

    @pytest.mark.parametrize('b', numbers)
    def test_add(self, b):
        assert _gmpy.mpz(1) + _gmpy.mpz(b) == _gmpy.mpz(1 + b)
        assert _gmpy.mpz(1) + b == _gmpy.mpz(1 + b)

    @pytest.mark.parametrize('b', numbers)
    def test_radd(self, b):
        assert b + _gmpy.mpz(1) == _gmpy.mpz(b + 1)

    @pytest.mark.parametrize('b', numbers)
    def test_sub(self, b):
        assert _gmpy.mpz(1) - _gmpy.mpz(b) == _gmpy.mpz(1 - b)
        assert _gmpy.mpz(1) - b == _gmpy.mpz(1 - b)

    @pytest.mark.parametrize('b', numbers)
    def test_rsub(self, b):
        assert b - _gmpy.mpz(1) == _gmpy.mpz(b - 1)
