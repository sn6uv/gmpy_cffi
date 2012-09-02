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
    numbers = {-1, 0, 1, sys.maxint, -sys.maxint - 1, 2 * sys.maxint + 1, 2 * sys.maxint + 2}

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
    def test_div(self, b):
        if b != 0:
            assert mpz(2) / mpz(b) == mpz(2 / b)
            assert mpz(2) / b == mpz(2 / b)
        else:
            with pytest.raises(ZeroDivisionError):
                mpz(2) / mpz(b)
            with pytest.raises(ZeroDivisionError):
                mpz(2) / b

    @pytest.mark.parametrize('b', numbers)
    def test_rdiv(self, b):
        assert b / mpz(2) == mpz(b / 2)
    def test_rdiv_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            1 / mpz(0)

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
