import sys
import _gmpy

class TestInit(object):
    small_ints = {-1, 0, 1, 123, -9876, sys.maxint, -sys.maxint - 1}
    big_ints = {sys.maxint + 1, -sys.maxint - 2, 2 * sys.maxint + 1, 2 * sys.maxint + 2}

    def _test_init(self, numbers):
        for n in numbers:
            _gmpy.mpz(n) == n

    def test_init_smallint(self):
        self._test_init(self.small_ints)

    def test_init_bigint(self):
        self._test_init(self.big_ints)

    def test_init_small_decimal_str(self):
        for n in self.small_ints:
            _gmpy.mpz(str(n), 10) == n
            _gmpy.mpz(str(n)) == n
            _gmpy.mpz(str(n), 0) == n

    def test_init_big_decimal_str(self):
        for n in self.big_ints:
            _gmpy.mpz(str(n), 10) == n
            _gmpy.mpz(str(n)) == n
            _gmpy.mpz(str(n), 0) == n

    def test_init_small_hex_str(self):
        for n in self.small_ints:
            _gmpy.mpz("%x" % n, 16) == n
            _gmpy.mpz("%#x" % n, 0) == n

    def test_init_big_hex_str(self):
        for n in self.big_ints:
            _gmpy.mpz("%x" % n, 16) == n
            _gmpy.mpz("%#x" % n, 0) == n
