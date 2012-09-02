from __future__ import division

import sys
import pytest
from _gmpy import mpz, MAX_UI

class TestInit(object):
    small_ints = {-1, 0, 1, 123, -9876, sys.maxint, -sys.maxint - 1}
    big_ints = {sys.maxint + 1, -sys.maxint - 2, 2 * sys.maxint + 1, 2 * sys.maxint + 2}

    @pytest.mark.parametrize('n', small_ints.union(big_ints))
    def test_init_int(self, n):
        assert mpz(n) == n

    @pytest.mark.parametrize('f', {0.0, 1.0, 1.5, 1e15 + 0.9})
    def test_init_float(self, f):
        assert mpz(f) == int(f)
        assert mpz(-f) == int(-f)

    @pytest.mark.parametrize('n', small_ints.union(big_ints))
    def test_init_decimal_str(self, n):
        assert mpz(str(n), 10) == n
        assert mpz(str(n)) == n
        assert mpz(str(n), 0) == n

    @pytest.mark.parametrize('n', small_ints.union(big_ints))
    def test_init_hex_str(self, n):
        assert mpz("%x" % n, 16) == n
        assert mpz("%#x" % n, 0) == n

    @pytest.mark.parametrize(('n', 'base'), {('0x1', 16), ('g', 16), ('a', 10)})
    def test_init_invalid_str(self, n, base):
        with pytest.raises(ValueError):
            mpz(n, base)

    @pytest.mark.parametrize(('n', 'base'), {('0', -1), ('0', 1), ('0', 63), (0, 10)})
    def test_init_invalid_base(self, n, base):
        with pytest.raises(ValueError):
            mpz(n, base)

    @pytest.mark.parametrize('type_', {int, float, mpz, str})
    def test_init_type(self, type_):
        assert mpz(type_(1)) == 1


class TestMath(object):
    numbers = {-1, 0, 1, sys.maxint, -sys.maxint - 1, MAX_UI, MAX_UI + 1}

    @pytest.mark.parametrize('b', numbers)
    def test_add(self, b):
        assert mpz(1) + mpz(b) == mpz(1 + b)
        assert mpz(1) + b == mpz(1 + b)

    @pytest.mark.parametrize('b', numbers)
    def test_radd(self, b):
        assert b + mpz(1) == mpz(b + 1)

    @pytest.mark.parametrize('b', numbers)
    def test_sub(self, b):
        assert mpz(1) - mpz(b) == mpz(1 - b)
        assert mpz(1) - b == mpz(1 - b)

    @pytest.mark.parametrize('b', numbers)
    def test_rsub(self, b):
        assert b - mpz(1) == mpz(b - 1)

    @pytest.mark.parametrize('b', numbers)
    def test_mul(self, b):
        assert mpz(2) * mpz(b) == mpz(2 * b)
        assert mpz(2) * b == mpz(2 * b)

    @pytest.mark.parametrize('b', numbers)
    def test_rmul(self, b):
        assert b * mpz(2) == mpz(b * 2)

    @pytest.mark.parametrize('b', numbers)
    def test_floordiv(self, b):
        if b != 0:
            assert mpz(2) // mpz(b) == mpz(2 // b)
            assert mpz(2) // b == mpz(2 // b)
        else:
            with pytest.raises(ZeroDivisionError):
                mpz(2) // mpz(b)
            with pytest.raises(ZeroDivisionError):
                mpz(2) // b

    @pytest.mark.parametrize('b', numbers)
    def test_rfloordiv(self, b):
        assert b // mpz(2) == mpz(b // 2)
    def test_rfloordiv_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            1 // mpz(0)

    @pytest.mark.xfail(reason='__truediv__ needs mpf')
    def test_truediv(self):
        assert mpz(3) / mpz(2) == 1.5

    @pytest.mark.parametrize('b', numbers)
    def test_mod(self, b):
        if b != 0:
            assert mpz(2) % mpz(b) == mpz(2 % b)
            assert mpz(2) % b == mpz(2 % b)
        else:
            with pytest.raises(ZeroDivisionError):
                mpz(2) % mpz(b)
            with pytest.raises(ZeroDivisionError):
                mpz(2) % b

    @pytest.mark.parametrize('b', numbers)
    def test_rmod(self, b):
        assert b % mpz(2) == mpz(b % 2)
    def test_rmod_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            1 % mpz(0)

    @pytest.mark.parametrize('b', numbers)
    def test_divmod(self, b):
        if b != 0:
            assert divmod(mpz(2), mpz(b)) == tuple(map(mpz, divmod(2, b)))
            assert divmod(mpz(2), b) == tuple(map(mpz, divmod(2, b)))
        else:
            with pytest.raises(ZeroDivisionError):
                divmod(mpz(2), mpz(b))
            with pytest.raises(ZeroDivisionError):
                divmod(mpz(2), b)

    @pytest.mark.parametrize('b', numbers)
    def test_rdivmod(self, b):
        assert divmod(b, mpz(2)) == tuple(map(mpz, divmod(b, 2)))
    def test_rdivmod_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            divmod(1, mpz(0))

    @pytest.mark.parametrize('b', {0, 2, 1 << 16})
    def test_shifts(self, b):
        assert mpz(1) << mpz(b) == mpz(1 << b)
        assert mpz(1) << b == mpz(1 << b)
        assert mpz(1 << 100) >> mpz(b) == mpz((1 << 100) >> b)
        assert mpz(1 << 100) >> b == mpz((1 << 100) >> b)

    @pytest.mark.parametrize('b', {0, 2, sys.maxint, MAX_UI})
    def test_rshifts(self, b):
        assert b << mpz(1) == mpz(b << 1)
        assert b >> mpz(1) == mpz(b >> 1)

    @pytest.mark.parametrize('b', {-1, MAX_UI + 1})
    def test_shifts_invalid_shift(self, b):
        with pytest.raises(OverflowError):
            mpz(1) << b
        with pytest.raises(OverflowError):
            mpz(1) >> b

    @pytest.mark.parametrize('type_', {int, long, mpz})
    def test_shifts_valid_type(self, type_):
        assert mpz(1) << type_(1) == mpz(2)
        assert mpz(4) >> type_(1) == mpz(2)

    @pytest.mark.parametrize('type_', {float, str})
    def test_shifts_invalid_type(self, type_):
        with pytest.raises(TypeError):
            mpz(1) << type_(1)
        with pytest.raises(TypeError):
            mpz(1) >> type_(1)

    @pytest.mark.parametrize('type_', {float, str})
    def test_rshifts_invalid_type(self, type_):
        with pytest.raises(TypeError):
            type_(1) << mpz(1)
        with pytest.raises(TypeError):
            type_(1) >> mpz(1)

    def test_str(self):
        n = mpz('123456789abcdef0', 16)
        assert str(n) == '1311768467463790320'
        assert repr(n) == 'mpz(1311768467463790320)'
        assert hex(n) == '0x123456789abcdef0'
        assert oct(n) == '0110642547423257157360'

    def test_conversions_int(self):
        for n in self.numbers:
            for type_ in {int, long}:
                n1 = type_(n)
                mpz_n = type_(mpz(n))
                assert type(n1) == type(mpz_n)
                assert n1 == mpz_n

    def test_conversion_float(self):
        for n in self.numbers:
            n1 = float(n)
            mpz_n = float(mpz(n))
            assert type(n1) == type(mpz_n)
            assert abs(n1 - mpz_n) <= abs(n1 * sys.float_info.epsilon)

    def test_conversion_complex(self):
        for n in self.numbers:
            n1 = complex(n)
            mpz_n = complex(mpz(n))
            assert type(n1) == type(mpz_n)
            assert abs(n1.real - mpz_n.real) <= abs(n1.real * sys.float_info.epsilon) and n1.imag == mpz_n.imag

    @pytest.mark.parametrize('n', numbers)
    def test_unary_methods(self, n):
        assert mpz(-n) == -mpz(n)
        assert mpz(+n) == +mpz(n)
        assert mpz(abs(n)) == abs(mpz(n))
        assert mpz(~n) == ~mpz(n)

    @pytest.mark.parametrize('n', numbers)
    def test_bit_ops(self, n):
        assert mpz(n) & mpz(n + 1) == mpz(n & (n + 1))
        assert mpz(n) & (n + 1) == mpz(n & (n + 1))
        assert mpz(n) | mpz(n + 1) == mpz(n | (n + 1))
        assert mpz(n) | (n + 1) == mpz(n | (n + 1))
        assert mpz(n) ^ mpz(n + 1) == mpz(n ^ (n + 1))
        assert mpz(n) ^ (n + 1) == mpz(n ^ (n + 1))

    @pytest.mark.parametrize('n', numbers)
    def test_bit_rops(self, n):
        assert n & mpz(n + 1) == mpz(n & (n + 1))
        assert n | mpz(n + 1) == mpz(n | (n + 1))
        assert n ^ mpz(n + 1) == mpz(n ^ (n + 1))

    def test_index(self):
        l = range(5)
        assert l[mpz(2)] == l[2]
        assert l[mpz(-1)] == l[-1]
        with pytest.raises(IndexError):
            l[mpz(10)]
            print "mist"

    def test_nonzero(self):
        assert mpz(23)
        assert not mpz(0)
        assert mpz(-1)

    @pytest.mark.parametrize('b', {-1, 0, 1, 1024, MAX_UI + 1})
    def test_pow_no_mod(self, b):
        if b < 0:
            for exp in {mpz(b), b}:
                with pytest.raises(ValueError) as exc:
                    mpz(2) ** exp
                assert exc.value.args == ('mpz.pow with negative exponent',)
        elif b > MAX_UI:
            for exp in {mpz(b), b}:
                with pytest.raises(ValueError) as exc:
                    mpz(2) ** exp
                assert exc.value.args == ('mpz.pow with outragous exponent',)
        else:
            res = mpz(2 ** b)
            assert mpz(2) ** mpz(b) == res
            assert mpz(2) ** b == res

    @pytest.mark.parametrize('b', {-1, 0, 1, 1024, MAX_UI + 1})
    def test_pow_with_mod(self, b):
        if b < 0:
            for exp in {mpz(b), b}:
                for mod in {mpz(7), 7}:
                    with pytest.raises(ValueError) as exc:
                        pow(mpz(2), exp, mod)
                    assert exc.value.args == ('mpz.pow with negative exponent',)
        else:
            res = mpz(pow(2, b, 7))
            assert pow(mpz(2), mpz(b), mpz(7)) == res
            assert pow(mpz(2), b, mpz(7)) == res
            assert pow(mpz(2), mpz(b), 7) == res
            assert pow(mpz(2), b, 7) == res

    @pytest.mark.parametrize('b', numbers)
    def test_rpow(self, b):
        assert b ** mpz(3) == mpz(b ** 3)

    def test_rpow_invalid(self):
        with pytest.raises(ValueError) as exc:
            1 ** mpz(-1)
        assert exc.value.args == ('mpz.pow with negative exponent',)
        with pytest.raises(ValueError) as exc:
            1 ** mpz(MAX_UI + 1)
        assert exc.value.args == ('mpz.pow with outragous exponent',)

    def test_pow_invalid(self):
        with pytest.raises(TypeError):
            mpz(2) ** 2.0
        with pytest.raises(TypeError):
            2.0 ** mpz(2)
        with pytest.raises(TypeError):
            pow(mpz(2), 2, 2.0)
