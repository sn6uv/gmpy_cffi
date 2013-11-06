from __future__ import division

import sys
import pytest
import itertools
from gmpy_cffi import mpq, mpz


class TestInit(object):
    ints = [1, -1, 2, -123, 456, sys.maxsize, -sys.maxsize - 1, 2*sys.maxsize, -2*sys.maxsize]
    floats = [0.0, 1.0, 1.5, 1e15 + 0.9, -1.5e15 + 0.9]
    pairs = itertools.combinations_with_replacement(ints, 2)

    # Length 0
    def test_init_empty(self):
        assert mpq() == mpq(0, 1)

    # Length 1
    @pytest.mark.parametrize('n', ints)
    def test_init_single_int(self, n):
        assert mpq(n) == n

    @pytest.mark.parametrize('f', floats)
    def test_init_float(self, f):
        assert float(mpq(f)) == f
        assert float(mpq(-f)) == -f

    @pytest.mark.parametrize('type_', [int, float, mpz, mpq, str])
    def test_init_type(self, type_):
        assert mpq(type_(1)) == 1


    @pytest.mark.parametrize('n', [[], set([])])
    def test_init_single_invalid(self, n):
        with pytest.raises(TypeError):
            mpq(n)

    @pytest.mark.parametrize('n', floats + [mpz(1), mpq(1, 2)])
    def test_init_zero_den(self, n):
        with pytest.raises(ZeroDivisionError):
            mpq(n, 0)

    # Length 2
    @pytest.mark.parametrize(('n', 'd'), pairs)
    def test_init_int_exact(self, n, d):
        assert float(mpq(n, d)) == n / d

    @pytest.mark.parametrize(('n', 'd'), pairs)
    def test_init_int_exact(self, n, d):
        assert float(mpq(n, d)) == n / d

    @pytest.mark.parametrize(('n', 'd'), [(1, 1), (-1, 1), (1, -1), (-1, -1)])
    def test_init_int(self, n, d):
        assert mpq(n, d) == n // d

    @pytest.mark.parametrize(('n', 'd'), pairs)
    def test_init_str(self, n, d):
        assert mpq('%s/%s' % (n, d)) == mpq(n, d)

    @pytest.mark.parametrize(('n', 'd'), pairs)
    def test_init_mpq(self, n, d):
        assert mpq(mpq(n, d)) == mpq(n, d)
        assert mpq(1, mpq(n, d)) == mpq(d, n)

    @pytest.mark.parametrize(('n', 'd'), pairs)
    def test_init_mpz(self, n, d):
        assert mpq(mpz(n), d) == mpq(n, d)
        assert mpq(n, mpz(d)) == mpq(n, d)
        assert mpq(mpz(n), mpz(d)) == mpq(n, d)

    @pytest.mark.parametrize(('n', 'base'), [('0x1', 16), ('g', 16), ('a', 10)])
    def test_init_invalid_str(self, n, base):
        with pytest.raises(ValueError):
            mpq(n, base)

    @pytest.mark.parametrize(('n', 'base'), [('0', -1), ('0', 1), ('0', 63)])
    def test_init_invalid_base(self, n, base):
        with pytest.raises(ValueError):
            mpq(n, base)

    # Invalid Length
    def test_invalid_nargs(self):
        with pytest.raises(TypeError):
            mpq(1,2,3)
        with pytest.raises(TypeError):
            mpq(1,2,3,4)
