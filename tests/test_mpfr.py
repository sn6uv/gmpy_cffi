import sys
import pytest

from gmpy_cffi import mpfr, mpq, mpz
from math import sqrt


invalids = [(), [], set(), dict(), lambda x: x**2]


class TestInit(object):
    ints = [0, -1, 1, 3, -25]

    def test_init_empty(self):
        assert mpfr() == mpfr('0.0')

    def test_init_str(self):
        assert mpfr('0.5') == mpfr(0.5)
        assert mpfr('1.5f99c8', 0, 16) == mpfr('1.3734402656555176')
        assert mpfr('1.5f99c8', 10, 16) == mpfr('1.373',10)

    @pytest.mark.parametrize('n', ints)
    def test_init_int(self, n):
        assert mpfr(int(n)) == mpfr(n)

    @pytest.mark.parametrize('n', ints)
    def test_init_mpz(self, n):
        assert mpfr(mpz(n)) == mpfr(n)

    def test_init_mpq(self):
        assert mpfr(mpq(2,3)) == mpfr('0.66666666666666663')


class TestMath(object):
    def test_repr(self):
        assert repr(mpfr(1.5)) == "mpfr('1.5')"
        assert repr(mpfr(-1.4)) == "mpfr('-1.3999999999999999')"
        assert repr(mpfr(2.5, 2)) == "mpfr('2.0',2)"
        assert repr(mpfr(2.5, 10)) == "mpfr('2.5',10)"
        assert repr(mpfr(2.5, 99)) == "mpfr('2.5',99)"
        assert repr(mpfr('nan')) == "mpfr('nan')"
        assert repr(mpfr('+inf')) == "mpfr('inf')"
        assert repr(mpfr('-inf')) == "mpfr('-inf')"

    def test_str(self):
        assert str(mpfr(1.5)) == '1.5'
        assert str(mpfr(-1.4)) == '-1.3999999999999999'
        assert str(mpfr(1.3, 21)) == '1.3000002'
        assert str(mpfr(1.3, 100)) == '1.3000000000000000444089209850063'
        assert str(mpfr('nan')) == 'nan'
        assert str(mpfr('+inf')) == 'inf'
        assert str(mpfr('-inf')) == '-inf'
