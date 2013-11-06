from __future__ import division

import sys
import pytest
from gmpy_cffi import mpq, mpz


class TestInit(object):
    int_pairs = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    rat_pairs = [(1, 2), (3, 4), (-123, 4567)]

    def test_init_empty(self):
        assert mpq() == mpq(0, 1)

    @pytest.mark.parametrize(('n', 'd'), int_pairs + rat_pairs)
    def test_init_int_exact(self, n, d):
        assert float(mpq(n, d)) == n / d

    @pytest.mark.parametrize(('n', 'd'), [(1, 1), (-1, 1), (1, -1), (-1, -1)])
    def test_init_int(self, n, d):
        assert mpq(n, d) == n // d

    @pytest.mark.parametrize('f', [0.0, 1.0, 1.5, 1e15 + 0.9])
    def test_init_float(self, f):
        assert float(mpq(f)) == f
        assert float(mpq(-f)) == -f

    @pytest.mark.parametrize(('n', 'd'), int_pairs + rat_pairs)
    def test_init_str(self, n, d):
        assert mpq('%s/%s' % (n, d)) == mpq(n, d)

    @pytest.mark.parametrize(('n', 'd'), int_pairs + rat_pairs)
    def test_init_mpq(self, n, d):
        assert mpq(mpq(n, d)) == mpq(n, d)
        assert mpq(1, mpq(n, d)) == mpq(d, n)

    @pytest.mark.parametrize(('n', 'd'), int_pairs + rat_pairs)
    def test_init_mpz(self, n, d):
        assert mpq(mpz(n), d) == mpq(n, d)
        assert mpq(n, mpz(d)) == mpq(n, d)
        assert mpq(mpz(n), mpz(d)) == mpq(n, d)

    @pytest.mark.parametrize('n', [-1, 0, 1, 1.5, 1e15, mpz(1), mpq(1, 2)])
    def test_init_zero_den(self, n):
        with pytest.raises(ZeroDivisionError):
            mpq(n, 0)

    @pytest.mark.parametrize(('n', 'base'), [('0x1', 16), ('g', 16), ('a', 10)])
    def test_init_invalid_str(self, n, base):
        with pytest.raises(ValueError):
            mpq(n, base)

    @pytest.mark.parametrize(('n', 'base'), [('0', -1), ('0', 1), ('0', 63), (0, 10)])
    def test_init_invalid_base(self, n, base):
        with pytest.raises(ValueError):
            mpq(n, base)

    @pytest.mark.parametrize('type_', [int, float, mpz, mpq, str])
    def test_init_type(self, type_):
        assert mpq(type_(1)) == 1
