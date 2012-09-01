import sys
import pytest
import _gmpy

class TestInit(object):
    small_ints = {-1, 0, 1, 123, -9876, sys.maxint, -sys.maxint - 1}
    big_ints = {sys.maxint + 1, -sys.maxint - 2, 2 * sys.maxint + 1, 2 * sys.maxint + 2}

    def _test_init(self, numbers):
        for n in numbers:
            assert _gmpy.mpz(n) == n

    def test_init_smallint(self):
        self._test_init(self.small_ints)

    def test_init_bigint(self):
        self._test_init(self.big_ints)

    def test_init_float(self):
        for f in {0.0, 1.0, 1.5, 1e15 + 0.9}:
            assert _gmpy.mpz(f) == int(f)
            assert _gmpy.mpz(-f) == int(-f)

    def test_init_small_decimal_str(self):
        for n in self.small_ints:
            assert _gmpy.mpz(str(n), 10) == n
            assert _gmpy.mpz(str(n)) == n
            assert _gmpy.mpz(str(n), 0) == n

    def test_init_big_decimal_str(self):
        for n in self.big_ints:
            assert _gmpy.mpz(str(n), 10) == n
            assert _gmpy.mpz(str(n)) == n
            assert _gmpy.mpz(str(n), 0) == n

    def test_init_small_hex_str(self):
        for n in self.small_ints:
            assert _gmpy.mpz("%x" % n, 16) == n
            assert _gmpy.mpz("%#x" % n, 0) == n

    def test_init_big_hex_str(self):
        for n in self.big_ints:
            assert _gmpy.mpz("%x" % n, 16) == n
            assert _gmpy.mpz("%#x" % n, 0) == n

    def test_init_invalid(self):
        for n, base in {('0x1', 16), ('g', 16), ('a', 10)}:
            with pytest.raises(ValueError):
                _gmpy.mpz(n, base)

class TestMath(object):
    numbers = {(0, 1), (23, 42), (sys.maxint, sys.maxint), (sys.maxint, 1)}

    def test_add(self):
        for a, b in self.numbers:
            assert _gmpy.mpz(a) + _gmpy.mpz(b) == _gmpy.mpz(a + b)
            assert _gmpy.mpz(a) + b == _gmpy.mpz(a + b)
            assert b + _gmpy.mpz(a) == _gmpy.mpz(b + a)
            assert (-a) + _gmpy.mpz(b) == _gmpy.mpz(-a + b)
            assert _gmpy.mpz(a) + (-b) == _gmpy.mpz(a - b)

    def test_sub(self):
        for a, b in self.numbers:
            assert _gmpy.mpz(a) - _gmpy.mpz(b) == _gmpy.mpz(a - b)
            assert _gmpy.mpz(a) - b == _gmpy.mpz(a - b)
            assert a - _gmpy.mpz(b) == _gmpy.mpz(a - b)
            #assert (-a) - _gmpy.mpz(b) == _gmpy.mpz(-a - b)
            assert _gmpy.mpz(a) - (-b) == _gmpy.mpz(a + b)
