from __future__ import division


import sys
import pytest
from gmpy_cffi import mpq, mpz, mpfr, mpc


PY3 = sys.version.startswith('3')


if PY3:
    long = int

class TestInit(object):
    # Length 0
    def test_init_empty(self):
        assert mpc() == mpc('0.0+0.0j')

    # Length 1
    def test_init_str1(self):
        assert mpc('1.5') == 1.5
        assert mpc('2') == 2
        assert mpc('1+0j') == 1+0j
        assert mpc('1.0+0.0j') == 1.0+0.0j
        assert mpc('1.0-0.0j') == 1.0-0.0j

    @pytest.mark.parametrize('c', (complex, mpc))
    def test_init_c1(self, c):
        assert mpc(c('1.0+0.5j')) == 1.0+0.5j

    @pytest.mark.parametrize('f', (float, mpfr))
    def test_init_f1(self, f):
        assert mpc(f(1.5)) == 1.5

    @pytest.mark.parametrize('i', (int, long, mpz))
    def test_init_i1(self, i):
        assert mpc(i(2)) == 2

    def test_init_q1(self):
        assert mpc(mpq(1,2)) == 0.5

    # Length 2
    def test_init_str2(self):
        x = mpc('1.5', 10)
        assert x == 1.5+0.0j
        assert x.precision == (10, 10)

        y = mpc('1.5+0.5j', 0)
        assert y == 1.5+0.5j
        assert y.precision == (53, 53)

    @pytest.mark.parametrize('c', (complex, mpc))
    def test_init_c2(self, c):
        assert mpc(c('1.0+0.5j'), 10) == 1.0+0.5j
        assert mpc(c('1.0+0.5j'), 10).precision == (10, 10)

    @pytest.mark.parametrize('f', (float, mpfr))
    def test_init_f2(self, f):
        assert mpc(f(1.5), 0.5) == 1.5+0.5j
        assert mpc(1.5, f(0.5)) == 1.5+0.5j
        assert mpc(f(1.5), f(0.5)) == 1.5+0.5j

    @pytest.mark.parametrize('i', (int, long, mpz))
    def test_init_i2(self, i):
        assert mpc(i(2), 3) == 2+3j
        assert mpc(2, i(3)) == 2+3j
        assert mpc(i(2), i(3)) == 2+3j

        # Increased Precision is required
        assert mpc(i(sys.maxsize), 0,  100) == sys.maxsize
        assert mpc(i(sys.maxsize+1), 0, 100) == sys.maxsize+1
        assert mpc(i(2*sys.maxsize), 0,  100) == 2*sys.maxsize
        assert mpc(i(3*sys.maxsize), 0, 100) == 3*sys.maxsize

    def test_init_q2(self):
        assert mpc(mpq(1,2), mpq(1,4)) == 0.5+0.25j
        assert mpc(mpq(1,2), 2) == 0.5+2j
        assert mpc(1, mpq(1,4)) == 1+0.25j

    # Length 3
    def test_init_str3(self):
        x = mpc('1.5+0.5j', 0, 10)
        assert x == 1.5+0.5j
        assert x.precision == (53, 53)

    @pytest.mark.parametrize('f', (float, mpfr))
    def test_init_f3(self, f):
        x = mpc(f(1.5), f(0.5), 100)
        assert x == 1.5+0.5j
        assert x.precision == (100, 100)

    @pytest.mark.parametrize('i', (int, long, mpz))
    def test_init_i3(self, i):
        x = mpc(i(2), i(3), 120)
        assert x == 2+3j
        assert x.precision == (120, 120)

    def test_init_q3(self):
        x = mpc(mpq(1,2), mpq(1,4), 110)
        assert x == 0.5+0.25j
        assert x.precision == (110, 110)

    # Invalid length
    def test_init_strn(self):
        with pytest.raises(TypeError):
            mpc('1.0+0.1j', 0, 10, 4)

    @pytest.mark.parametrize('c', (complex, mpc))
    def test_init_cn(self, c):
        with pytest.raises(TypeError):
            assert mpc(c('1.0+0.5j'), 10, 10) == 1.0+0.5j

    @pytest.mark.parametrize('c', (complex, mpc))
    def test_init_cn(self, c):
        with pytest.raises(TypeError):
            mpc(c('1.0+0.5j'), 10, 10) == 1.0+0.5j

    @pytest.mark.parametrize('f', (float, mpfr))
    def test_init_fn(self, f):
        with pytest.raises(TypeError):
            mpc(f(1.5), f(0.5), 10, 10)

    @pytest.mark.parametrize('i', (int, long, mpz))
    def test_init_in(self, i):
        with pytest.raises(TypeError):
            mpc(i(2), i(3), 10, 10)

    def test_init_qn(self):
        with pytest.raises(TypeError):
            mpc(mpq(1,2), mpq(1,4), 10, 10)

    # Misc
    def test_precision(self):
        assert mpc(1.5, 2.3, 100).precision == (100, 100)
        assert mpc(1.5, 2.3, (100, 110)).precision == (100, 110)
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, (100, 110, 120))
        assert mpc(1.5, 2.3, 0).precision == (53, 53)
        assert mpc(1.5, 2.3, (0, 20)).precision == (53, 20)
        assert mpc(1.5, 2.3, (20, 0)).precision == (20, 53)
        assert mpc(1.5, 2.3, (0, 0)).precision == (53, 53)
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, 1)
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, -1)
        mpc(1.5, 2.3, 2)    # shouldn't raise
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, (-1, 100))
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, (100, -1))
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, (100, sys.maxsize+1))
        with pytest.raises(ValueError):
            mpc(1.5, 2.3, (sys.maxsize+1, 100))

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            mpc(1.5, [])
        with pytest.raises(TypeError):
            mpc([], 1.5)

    def test_real(self):
        assert mpc(1.5, 2.3).real == 1.5

    def test_imag(self):
        assert mpc(1.5, 2.3).imag == 2.3

    def test_repr(self):
        assert repr(mpc(1.5, 1.3)) == "mpc('1.5+1.3j')"
        assert repr(mpc(1.5, 2.3)) == "mpc('1.5+2.2999999999999998j')"
        assert repr(mpc(1.4, 2.3)) == "mpc('1.3999999999999999+2.2999999999999998j')"
        assert repr(mpc(1.5, 2.3, 100)) == "mpc('1.5+2.299999999999999822364316059975j',(100,100))"
        assert repr(mpc(1.5, 2.3, (0, 60))) == "mpc('1.5+2.2999999999999998224j',(53,60))"
        assert repr(mpc(1.5, 2.3, (60, 0))) == "mpc('1.5+2.2999999999999998j',(60,53))"
        assert repr(mpc(1.5, 2.3, 53)) == "mpc('1.5+2.2999999999999998j')"


class TestCmp(object):

    @pytest.mark.parametrize('c', (complex, mpc))
    def test_c(self, c):
        # Left Comparison
        with pytest.raises(TypeError):
            assert mpc('1.5+2.5j') > c('1.5+2.5j')
        with pytest.raises(TypeError):
            assert mpc('1.5+2.5j') < c('1.5+2.5j')
        with pytest.raises(TypeError):
            assert mpc('1.5+2.5j') >= c('1.5+2.5j')
        with pytest.raises(TypeError):
            assert mpc('1.5+2.5j') <= c('1.5+2.5j')
        assert mpc('1.5+2.5j') == c('1.5+2.5j')
        assert mpc('1.5+2.5j') != c('1.4+2.5j')
        assert mpc('1.5+2.5j') != c('1.5+2.4j')

    @pytest.mark.parametrize('f', (float, mpfr))
    def test_f(self, f):
        # Left Comparison
        with pytest.raises(TypeError):
            assert mpc('1.5') > f('1.5')
        with pytest.raises(TypeError):
            assert mpc('1.5') < f('1.5')
        with pytest.raises(TypeError):
            assert mpc('1.5') >= f('1.5')
        with pytest.raises(TypeError):
            assert mpc('1.5') <= f('1.5')
        assert mpc('1.5') == f('1.5')
        assert mpc('1.5') != f('1.4')
        assert mpc('1.5+0.1j') != f('1.5')

    @pytest.mark.parametrize('i', (int, long, mpz))
    def test_i(self, i):
        # Left Comparison
        with pytest.raises(TypeError):
            assert mpc('2') > i('3')
        with pytest.raises(TypeError):
            assert mpc('2') < i('3')
        with pytest.raises(TypeError):
            assert mpc('2') >= i('3')
        with pytest.raises(TypeError):
            assert mpc('2') <= i('3')
        assert mpc('2') == i('2')
        assert mpc('2') != i('3')
        assert mpc('2+1j') != i('2')

        # Increased precision is required for large ints
        assert mpc(sys.maxsize, 0, 100) == i(sys.maxsize)
        assert mpc(sys.maxsize+1, 0, 100) == i(sys.maxsize+1)
        assert mpc(2*sys.maxsize, 0, 100) == i(2*sys.maxsize)
        assert mpc(3*sys.maxsize, 0, 100) == i(3*sys.maxsize)
        assert mpc(sys.maxsize, 0, 100) != i(sys.maxsize-1)
        assert mpc(sys.maxsize+1, 0, 100) != i(sys.maxsize)
        assert mpc(2*sys.maxsize, 0, 100) != i(2*sys.maxsize-1)
        assert mpc(3*sys.maxsize, 0, 100) != i(3*sys.maxsize-1)

    def test_q(self):
        with pytest.raises(TypeError):
            mpc('0.5') > mpq(1,2)
        with pytest.raises(TypeError):
            mpc('0.5') < mpq(1,2)
        with pytest.raises(TypeError):
            mpc('0.5') >= mpq(1,2)
        with pytest.raises(TypeError):
            mpc('0.5') <= mpq(1,2)
        assert mpc('0.5') == mpq(1,2)
        assert mpc('0.4') != mpq(1,2)
        assert mpc('0.5+0.25j') != mpq(1,2)

    def test_invalid(self):
        assert not mpc(1) == []
        with pytest.raises(TypeError):
            mpc('0.5') > []


class TestConv(object):
    def test_float(self):
        with pytest.raises(TypeError):
            float(mpc('1.5+0.5j'))
        with pytest.raises(TypeError):
            float(mpc('1.5'))

    def test_int(self):
        with pytest.raises(TypeError):
            int(mpc('1.5'))

    def test_long(self):
        with pytest.raises(TypeError):
            long(mpc('1.5'))

    @pytest.mark.xfail("sys.version.startswith('2.6')", reason="python2.6 complex")
    def test_complex(self):
        complex(mpc('1.5+0.5j')) == 1.5+0.5j
        complex(mpc('1.5-0.5j')) == 1.5-0.5j
        complex(mpc('nan+0.5j')) == complex('nan+0.5j')
        complex(mpc('0.5+nanj')) == complex('0.5+nanj')
        complex(mpc('nan+nanj')) == complex('nan+nanj')
        complex(mpc('inf+0.5j')) == complex('inf+0.5j')
        complex(mpc('0.5+infj')) == complex('0.5+infj')
        complex(mpc('inf-infj')) == complex('inf-infj')


class TestMath(object):
    def test_add(self):
        assert mpc('1.5+0.5j') + mpc('0.2+0.3j') == mpc('1.7+0.8j')
        assert mpc('1.5+0.5j') + (0.2+0.3j) == mpc('1.7+0.8j')
        assert mpc('1.5+0.5j') + mpfr('1.5') == mpc('3.0+0.5j')
        assert mpc('1.5+0.5j') + mpq(3, 2) == mpc('3.0+0.5j')
        assert mpc('1.5+0.5j') + mpz(2) == mpc('3.5+0.5j')
        assert mpc('1.5+0.5j') + 1.5 == mpc('3.0+0.5j')
        assert mpc('1.5+0.5j') + 1 == mpc('2.5+0.5j')
        assert mpc('1.5+0.5j') + (-1) == mpc('0.5+0.5j')
        assert mpc('1.2e19') + sys.maxsize == mpc('2.1223372036854776e19')
        assert mpc('1.2e19') + 2*sys.maxsize == mpc('3.0446744073709552e+19')
        assert mpc('1.2e19') + 3*sys.maxsize == mpc('3.9670116110564327e+19')
        with pytest.raises(TypeError):
            assert mpc('1.5+0.5j') + []
        assert 1.5 + mpc('1.5+0.5j') == mpc('3.0+0.5j')

    def test_sub(self):
        assert mpc('1.5+0.5j') - mpc('0.2+0.3j') == mpc('1.3+0.2j')
        assert mpc('1.5+0.5j') - (0.2+0.3j) == mpc('1.3+0.2j')
        assert mpc('1.5+0.5j') - mpfr('0.2') == mpc('1.3+0.5j')
        assert mpc('1.5+0.5j') - mpq(3, 2) == mpc('0.0+0.5j')
        assert mpc('1.5+0.5j') - mpz(2) == mpc('-0.5+0.5j')
        assert mpc('1.5+0.5j') - 1.5 == mpc('0.0+0.5j')
        assert mpc('1.5+0.5j') - 1 == mpc('0.5+0.5j')

        assert mpc('1.5+0.5j') - (-1) == mpc('2.5+0.5j')
        assert mpc('3.2e19') - sys.maxsize == mpc('2.2776627963145224e+19')
        assert mpc('3.2e19') - 2*sys.maxsize == mpc('1.3553255926290448e+19')
        assert mpc('3.2e19') - 3*sys.maxsize == mpc('4.3298838894356726e+18')
        with pytest.raises(TypeError):
            assert mpc('1.5+0.5j') - []

    def test_rsub(self):
        assert mpfr('1.5') - mpc('0.5') == mpc('1.0')
        assert (1.5+0.5j) - mpc('0.2+0.3j') == mpc('1.3+0.2j')
        assert 1.5 - mpc('0.5') == mpc('1.0')
        assert mpq(3,2) - mpc('0.5') == mpc('1.0')
        assert mpz(1) - mpc('0.5') == mpc('0.5')
        assert 1 - mpc('0.5') == mpc('0.5')
        assert (-1) - mpc('0.5') == mpc('-1.5')
        assert sys.maxsize - mpc('1.2e19') == mpc('-2.7766279631452242e+18')
        assert 2*sys.maxsize - mpc('1.2e19') == mpc('6.4467440737095516e+18')
        assert 3*sys.maxsize - mpc('1.2e19') == mpc('1.5670116110564327e+19')
        with pytest.raises(TypeError):
            [] - mpc('1.5+0.5j')

    def test_mul(self):
        assert mpc('0.5+0.1j') * mpc('0.5+0.2j') == mpc('0.23+0.15000000000000002j')
        assert mpc('0.5+0.1j') * (0.5+0.2j) == mpc('0.23+0.15000000000000002j')

        assert mpc('0.5+0.3j') * mpfr('1.5') == mpc('0.75+0.44999999999999996j')
        assert mpc('0.5+0.3j') * 1.5 == mpc('0.75+0.44999999999999996j')
        assert mpc('0.5+0.3j') * mpq(3,2) == mpc('0.75+0.44999999999999996j')
        assert mpc('0.5+0.3j') * mpz(3) == mpc('1.5+0.89999999999999991j')
        assert mpc('0.5+0.3j') * 3 == mpc('1.5+0.89999999999999991j')
        assert mpc('1.5') * sys.maxsize == mpc('1.3835058055282164e+19')
        assert mpc('1.5') * (2 * sys.maxsize) == mpc('2.7670116110564327e+19')
        assert mpc('1.5') * (3 * sys.maxsize) == mpc('4.1505174165846491e+19')
        with pytest.raises(TypeError):
            mpc('1.5+0.5j') * []
        assert 3 * mpc('1.5+0.5j') == mpc('4.5+1.5j')
