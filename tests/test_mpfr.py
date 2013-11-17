from __future__ import division

import sys
import math
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
        assert mpfr(mpq(2,5),80) == mpfr('0.40000000000000000000000008',80)


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

    def test_add(self):
        assert mpfr('0.5') + mpfr('1.5') == mpfr('2.0')
        assert mpfr('0.5') + 1.5 == mpfr('2.0')
        assert mpfr('0.5') + mpq(3,2) == mpfr('2.0')
        assert mpfr('0.5') + mpz(1) == mpfr('1.5')
        assert mpfr('0.5') + 1 == mpfr('1.5')
        assert mpfr('1.2e19') + sys.maxsize == mpfr('2.1223372036854776e+19')
        assert mpfr('1.2e19') + 2*sys.maxsize == mpfr('3.0446744073709552e+19')
        assert mpfr('1.2e19') + 3*sys.maxsize == mpfr('3.9670116110564327e+19')

    def test_sub(self):
        assert mpfr('1.5') - mpfr('0.5') == mpfr('1.0')
        assert mpfr('1.5') - 0.5 == mpfr('1.0')
        assert mpfr('1.5') - mpq(1,2) == mpfr('1.0')
        assert mpfr('1.5') - mpz(1) == mpfr('0.5')
        assert mpfr('1.5') - 1 == mpfr('0.5')
        assert mpfr('3.2e19') - sys.maxsize == mpfr('2.2776627963145224e+19')
        assert mpfr('3.2e19') - 2 * sys.maxsize == mpfr('1.3553255926290448e+19')
        assert mpfr('3.2e19') - 3 * sys.maxsize == mpfr('4.3298838894356726e+18')

    def test_rsub(self):
        assert 1.5 - mpfr('0.5') == mpfr('1.0')
        assert mpq(3,2) - mpfr('0.5') == mpfr('1.0')
        assert mpz(1) - mpfr('0.5') == mpfr('0.5')
        assert 1 - mpfr('0.5') == mpfr('0.5')
        assert sys.maxsize - mpfr('1.2e19') == mpfr('-2.7766279631452242e+18')
        assert 2*sys.maxsize - mpfr('1.2e19') == mpfr('6.4467440737095516e+18')
        assert 3*sys.maxsize - mpfr('1.2e19') == mpfr('1.5670116110564327e+19')

    def test_mul(self):
        assert mpfr('0.5') * mpfr('1.5') == mpfr('0.75')
        assert mpfr('0.5') * 1.5 == mpfr('0.75')
        assert mpfr('0.5') * mpq(3,2) == mpfr('0.75')
        assert mpfr('0.5') * mpz(3) == mpfr('1.5')
        assert mpfr('0.5') * 3 == mpfr('1.5')
        assert mpfr('1.5') * sys.maxsize == mpfr('1.3835058055282164e+19')
        assert mpfr('1.5') * (2 * sys.maxsize) == mpfr('2.7670116110564327e+19')
        assert mpfr('1.5') * (3 * sys.maxsize) == mpfr('4.1505174165846491e+19')

    def test_truediv(self):
        assert mpfr('1.5') / mpfr('0.5') == mpfr('3.0')
        assert mpfr('1.5') / 0.5 == mpfr('3.0')
        assert mpfr('1.5') / mpq(3,2) == mpfr('1.0')
        assert mpfr('4.5') / mpz(3) == mpfr('1.5')
        assert mpfr('4.5') / 3 == mpfr('1.5')
        assert mpfr('1.5e19') / sys.maxsize == mpfr('1.6263032587282567')
        assert mpfr('1.5e19') / (2 * sys.maxsize) == mpfr('0.81315162936412833')
        assert mpfr('1.5e19') / (3 * sys.maxsize) == mpfr('0.54210108624275222')

    def test_rtruediv(self):
        assert 1.5 / mpfr('0.5') == mpfr('3.0')
        assert mpq(3,2) / mpfr('0.5') == mpfr('3.0')
        assert mpz(3) / mpfr('1.5') == mpfr('2.0')
        assert 3 / mpfr('1.5') == mpfr('2.0')
        assert sys.maxsize / mpfr(1.5e19) == mpfr('0.61489146912365167')
        assert (2 * sys.maxsize) / mpfr(1.5e19) == mpfr('1.2297829382473033')
        assert (3 * sys.maxsize) / mpfr(1.5e19) == mpfr('1.8446744073709551')

    def test_pow(self):
        assert mpfr('2.5') ** mpfr('1.5') == mpfr('3.9528470752104741')
        assert mpfr('2.5') ** 1.5 == mpfr('3.9528470752104741')
        assert mpfr('2.5') ** mpq(3,2) == mpfr('3.9528470752104741')
        assert mpfr('2.5') ** mpz(3) == mpfr('15.625')
        assert mpfr('2.5') ** 3 == mpfr('15.625')
        assert mpfr('1.5') ** sys.maxsize == mpfr('inf')
        assert mpfr('1.5') ** (2 * sys.maxsize) == mpfr('inf')
        assert mpfr('1.5') ** (3 * sys.maxsize) == mpfr('inf')
        assert mpfr('1.0') ** sys.maxsize == mpfr('1.0')
        assert mpfr('1.0') ** (2 * sys.maxsize) == mpfr('1.0')
        assert mpfr('1.0') ** (3 * sys.maxsize) == mpfr('1.0')

    def test_rpow(self):
        assert 1.5 ** mpfr('2.5') == mpfr('2.7556759606310752')
        assert mpq(3,2) ** mpfr('2.5') == mpfr('2.7556759606310752')
        assert mpz(3) ** mpfr('2.5') == mpfr('15.588457268119896')
        assert 3 ** mpfr('2.5') == mpfr('15.588457268119896')
        assert sys.maxsize ** mpfr(1.5) == mpfr('2.8011385487393072e+28')
        assert (2 * sys.maxsize) ** mpfr(1.5) == mpfr('7.9228162514264338e+28')
        assert (3 * sys.maxsize) ** mpfr(1.5) == mpfr('1.4555142856368689e+29')

    def test_neg(self):
        assert -mpfr(1.5) == mpfr(-1.5)
        assert -mpfr(-1.5) == mpfr(1.5)
        assert -mpfr('0') == mpfr('-0')
        assert -mpfr('-0') == mpfr('0')
        assert -mpfr('inf') == mpfr('-inf')
        assert -mpfr('-inf') == mpfr('inf')
        assert -mpfr('nan') == mpfr('nan')

    def test_pos(self):
        assert +mpfr(1.5) == mpfr(1.5)
        assert +mpfr(-1.5) == mpfr(-1.5)
        assert +mpfr('0') == mpfr('0')
        assert +mpfr('-0') == mpfr('-0')
        assert +mpfr('inf') == mpfr('inf')
        assert +mpfr('-inf') == mpfr('-inf')
        assert +mpfr('nan') == mpfr('nan')

    def test_abs(self):
        assert abs(mpfr(1.5)) == mpfr(1.5)
        assert abs(mpfr(-1.5)) == mpfr(1.5)
        assert abs(mpfr('0')) == mpfr('0')
        assert abs(mpfr('-0')) == mpfr('0')
        assert abs(mpfr('inf')) == mpfr('inf')
        assert abs(mpfr('-inf')) == mpfr('inf')
        assert abs(mpfr('nan')) == mpfr('nan')

    def test_floor(self):
        assert math.floor(mpfr(1.5)) == 1.0
        assert math.floor(mpfr(-1.5)) == -2.0
        assert math.floor(mpfr('inf')) == float('inf')
        assert math.floor(mpfr('-inf')) == float('-inf')
        assert math.isnan(math.floor(mpfr('nan')))

    def test_ceil(self):
        assert math.ceil(mpfr(1.5)) == 2.0
        assert math.ceil(mpfr(-1.5)) == -1.0
        assert math.ceil(mpfr('inf')) == float('inf')
        assert math.ceil(mpfr('-inf')) == float('-inf')
        assert math.isnan(math.ceil(mpfr('nan')))

    def test_trunc(self):
        assert math.trunc(mpfr(1.5)) == 1.0
        assert math.trunc(mpfr(-1.5)) == -1.0
        assert math.trunc(mpfr('inf')) == float('inf')
        assert math.trunc(mpfr('-inf')) == float('-inf')
        assert math.isnan(math.trunc(mpfr('nan')))


class TestConv(object):
    @pytest.mark.parametrize('n', ['1.5', '0.0', '-0.0', 'inf', '-inf', 'nan'])
    def test_float(self, n):
        if n == 'nan': # float('nan') != float('nan')
            assert math.isnan(float(mpfr(n)))
        else:
            assert float(mpfr(n)) == float(n)

    def test_int(self):
        assert int(mpfr(1.4)) == 1
        assert int(mpfr(1.6)) == 2
        assert int(mpfr(-1.4)) == -1
        assert int(mpfr(-1.6)) == -2
