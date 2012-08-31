import sys
import _gmpy

class TestInit(object):
    def _test_init(self, numbers):
        for n in numbers:
            _gmpy.mpz(n) == n

    def test_init_smallint(self):
        self._test_init({-1, 0, 1, 123, -9876, sys.maxint, -sys.maxint - 1})

    def test_init_bigint(self):
        self._test_init({sys.maxint + 1, -sys.maxint - 2, 2 * sys.maxint + 1, 2 * sys.maxint + 2})
