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
    def test_init_invalid(self, n, base):
        with pytest.raises(ValueError):
            _gmpy.mpz(n, base)

class TestMath(object):
    numbers = {(0, 1), (23, 42), (sys.maxint, sys.maxint), (sys.maxint, 1)}

    @pytest.mark.parametrize(('a', 'b'), numbers)
    def test_add(self, a, b):
        assert _gmpy.mpz(a) + _gmpy.mpz(b) == _gmpy.mpz(a + b)
        assert _gmpy.mpz(a) + b == _gmpy.mpz(a + b)
        assert b + _gmpy.mpz(a) == _gmpy.mpz(b + a)
        assert (-a) + _gmpy.mpz(b) == _gmpy.mpz(-a + b)
        assert _gmpy.mpz(a) + (-b) == _gmpy.mpz(a - b)

    @pytest.mark.parametrize(('a', 'b'), numbers)
    def test_sub(self, a, b):
        if a:
            pytest.xfail('a != 0')
        assert _gmpy.mpz(a) - _gmpy.mpz(b) == _gmpy.mpz(a - b)
        assert _gmpy.mpz(a) - b == _gmpy.mpz(a - b)
        assert a - _gmpy.mpz(b) == _gmpy.mpz(a - b)
        assert (-a) - _gmpy.mpz(b) == _gmpy.mpz(-a - b)
        assert _gmpy.mpz(a) - (-b) == _gmpy.mpz(a + b)
