import sys
import pytest
from gmpy_cffi import mpq, mpz


invalids = [(), [], set(), dict(), lambda x: x**2]


class TestInit(object):
    ints = [1, -1, 2, -123, 456, sys.maxsize, -sys.maxsize - 1, 2*sys.maxsize, -2*sys.maxsize]
    floats = [0.0, 1.0, 1.5, 1e15 + 0.9, -1.5e15 + 0.9]
    int_pairs = [(i,j) for i in ints for j in ints]

    # Length 0
    def test_init_empty(self):
        assert mpq() == mpq(0, 1)

    # Length 1
    @pytest.mark.parametrize('n', ints)
    def test_init_int1(self, n):
        assert mpq(n) == n

    @pytest.mark.parametrize('f', floats)
    def test_init_float1(self, f):
        assert float(mpq(f)) == f
        assert float(mpq(-f)) == -f

    @pytest.mark.parametrize(('n', 'd'), int_pairs)
    def test_init_mpq1(self, n, d):
        assert mpq(mpq(n, d)) == mpq(n, d)

    @pytest.mark.parametrize('type_', [int, float, mpz, mpq, str])
    def test_init_type(self, type_):
        assert mpq(type_(1)) == 1

    @pytest.mark.parametrize('n', invalids)
    def test_init_single_invalid(self, n):
        with pytest.raises(TypeError):
            mpq(n)

    @pytest.mark.parametrize('n', floats + [mpz(1), mpq(1, 2)])
    def test_init_zero_den(self, n):
        with pytest.raises(ZeroDivisionError):
            mpq(n, 0)

    # Length 2
    @pytest.mark.parametrize(('n', 'd'), [(1, 1), (-1, 1), (1, -1), (-1, -1)])
    def test_init_sign(self, n, d):
        assert mpq(n, d) == n / d

    @pytest.mark.parametrize(('n', 'd'), int_pairs)
    def test_init_str(self, n, d):
        assert mpq('%s/%s' % (n, d)) == mpq(n, d)
        assert mpq(1, mpq(n, d)) == mpq(d, n)

    def test_init_int2(self):
        assert mpq(3, 6) == mpq(1, 2)
        assert mpq(2, sys.maxsize) == mpq(2, sys.maxsize)
        assert mpq(4, 2*sys.maxsize) == mpq(2, sys.maxsize)
        assert mpq(8, 4*sys.maxsize) == mpq(2, sys.maxsize)
        assert mpq(3, mpz(5)) == mpq(3, 5)
        assert mpq(3, mpq(5, 7)) == mpq(21, 5)
        assert mpq(3, 0.5) == mpq(6, 1)
        assert mpq(3, 0.6) == mpq(27021597764222976,5404319552844595)

        assert mpq(sys.maxsize, 6) == mpq(sys.maxsize, 6)
        assert mpq(sys.maxsize, sys.maxsize) == mpq(1, 1)
        assert mpq(sys.maxsize, 2*sys.maxsize) == mpq(1, 2)
        assert mpq(sys.maxsize, 4*sys.maxsize) == mpq(1, 4)
        assert mpq(sys.maxsize, mpz(5)) == mpq(sys.maxsize, 5)
        assert mpq(sys.maxsize, mpq(5, 7)) == mpq(7*sys.maxsize, 5)
        assert mpq(sys.maxsize, 0.5) == mpq(2*sys.maxsize, 1)
        assert mpq(sys.maxsize, 0.6) == mpq(9007199254740992*sys.maxsize, 5404319552844595)

        assert mpq(2*sys.maxsize, 6) == mpq(2*sys.maxsize, 6)
        assert mpq(2*sys.maxsize, sys.maxsize) == mpq(2, 1)
        assert mpq(2*sys.maxsize, 2*sys.maxsize) == mpq(1, 1)
        assert mpq(2*sys.maxsize, 4*sys.maxsize) == mpq(1, 2)
        assert mpq(2*sys.maxsize, mpz(5)) == mpq(2*sys.maxsize, 5)
        assert mpq(2*sys.maxsize, mpq(5, 7)) == mpq(14*sys.maxsize, 5)
        assert mpq(2*sys.maxsize, 0.5) == mpq(4*sys.maxsize, 1)
        assert mpq(2*sys.maxsize, 0.6) == mpq(2*9007199254740992*sys.maxsize, 5404319552844595)

        assert mpq(4*sys.maxsize, 6) == mpq(2*sys.maxsize, 3)
        assert mpq(4*sys.maxsize, sys.maxsize) == mpq(4, 1)
        assert mpq(4*sys.maxsize, 2*sys.maxsize) == mpq(2, 1)
        assert mpq(4*sys.maxsize, 4*sys.maxsize) == mpq(1, 1)
        assert mpq(4*sys.maxsize, mpz(5)) == mpq(4*sys.maxsize, 5)
        assert mpq(4*sys.maxsize, mpq(5, 7)) == mpq(28*sys.maxsize, 5)
        assert mpq(4*sys.maxsize, 0.5) == mpq(8*sys.maxsize, 1)
        assert mpq(4*sys.maxsize, 0.6) == mpq(4*9007199254740992*sys.maxsize, 5404319552844595)

    def test_init_mpz(self):
        assert mpq(mpz(3), 6) == mpq(1, 2)
        assert mpq(mpz(2), sys.maxsize) == mpq(2, sys.maxsize)
        assert mpq(mpz(4), 2*sys.maxsize) == mpq(2, sys.maxsize)
        assert mpq(mpz(8), 4*sys.maxsize) == mpq(2, sys.maxsize)
        assert mpq(mpz(3), mpz(5)) == mpq(3, 5)
        assert mpq(mpz(3), mpq(5, 7)) == mpq(21, 5)
        assert mpq(mpz(3), 0.5) == mpq(6, 1)
        assert mpq(mpz(3), 0.6) == mpq(27021597764222976,5404319552844595)

    def test_init_mpq2(self):
        assert mpq(mpq(2, 3), 1) == mpq(2, 3)
        assert mpq(mpq(2, 3), sys.maxsize) == mpq(2, 3*sys.maxsize)
        assert mpq(mpq(2, 3), 2*sys.maxsize) == mpq(1, 3*sys.maxsize)
        assert mpq(mpq(2, 3), 5*sys.maxsize) == mpq(2, 15*sys.maxsize)
        assert mpq(mpq(2, 3), mpz(5)) == mpq(2, 15)
        assert mpq(mpq(2, 3), mpq(5, 7)) == mpq(14, 15)
        assert mpq(mpq(2, 3), 0.5) == mpq(4, 3)
        assert mpq(mpq(2, 3), 0.6) == mpq(18014398509481984,16212958658533785)

    def test_init_float2(self):
        assert mpq(0.5, 1) == mpq(1, 2)
        assert mpq(0.5, sys.maxsize) == mpq(1, 2*sys.maxsize)
        assert mpq(0.5, 2*sys.maxsize) == mpq(1, 4*sys.maxsize)
        assert mpq(0.5, 5*sys.maxsize) == mpq(1, 10*sys.maxsize)
        assert mpq(0.5, mpz(5)) == mpq(1, 10)
        assert mpq(0.5, mpq(5, 7)) == mpq(7, 10)
        assert mpq(0.5, 0.5) == mpq(1, 1)
        assert mpq(0.5, 0.6) == mpq(4503599627370496,5404319552844595)

        assert mpq(0.6, 1) == mpq(5404319552844595,9007199254740992)
        assert mpq(0.6, sys.maxsize) == mpq(5404319552844595, 9007199254740992*sys.maxsize)
        assert mpq(0.6, 2*sys.maxsize) == mpq(5404319552844595, 2*9007199254740992*sys.maxsize)
        assert mpq(0.6, 5*sys.maxsize) == mpq(5404319552844595, 5*9007199254740992*sys.maxsize)
        assert mpq(0.6, mpz(5)) == mpq(1080863910568919,9007199254740992)
        assert mpq(0.6, mpq(5, 7)) == mpq(7566047373982433,9007199254740992)
        assert mpq(0.6, 0.5) == mpq(5404319552844595,4503599627370496)
        assert mpq(0.6, 0.6) == mpq(1, 1)

    @pytest.mark.parametrize('n', invalids)
    def test_init_single_num(self, n):
        with pytest.raises(TypeError):
            mpq(n, 1)

    @pytest.mark.parametrize('d', invalids)
    def test_init_single_den(self, d):
        with pytest.raises(TypeError):
            mpq(1, d)

    @pytest.mark.parametrize('n', [3, sys.maxsize, 2*sys.maxsize, 5*sys.maxsize, 1.5, mpz(13)])
    def test_init_zero_den2(self, n):
        with pytest.raises(ZeroDivisionError):
            mpq(n, 0)
        with pytest.raises(ZeroDivisionError):
            mpq(n, 0.0)
        with pytest.raises(ZeroDivisionError):
            mpq(n, mpz(0))
        with pytest.raises(ZeroDivisionError):
            mpq(n, mpq(0,1))

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


class TestMath(object):

    def test_add(self):
        assert mpq(1, 2) + mpq(1, 3) == mpq(5, 6)
        assert mpq(1, 2) + 2 == mpq(5, 2)
        assert mpq(1, 2) + sys.maxsize == mpq(2*sys.maxsize + 1, 2)
        assert mpq(1, 2) + 2*sys.maxsize == mpq(4*sys.maxsize + 1, 2)
        assert mpq(1, 2) + 3*sys.maxsize == mpq(6*sys.maxsize + 1, 2)
        assert mpq(1, 2) + mpz(2) == mpq(5, 2)

    def test_radd(self):
        assert mpq(1, 3) + mpq(1, 2) == mpq(5, 6)
        assert 2 + mpq(1, 2) == mpq(5, 2)
        assert sys.maxsize + mpq(1, 2) == mpq(2*sys.maxsize + 1, 2)
        assert 2*sys.maxsize + mpq(1, 2) == mpq(4*sys.maxsize + 1, 2)
        assert 3*sys.maxsize + mpq(1, 2) == mpq(6*sys.maxsize + 1, 2)
        assert mpz(2) + mpq(1, 2) == mpq(5, 2)

    def test_sub(self):
        assert mpq(1, 2) - mpq(1, 3) == mpq(1, 6)
        assert mpq(1, 2) - 2 == mpq(-3, 2)
        assert mpq(1, 2) - sys.maxsize == mpq(1 - 2*sys.maxsize, 2)
        assert mpq(1, 2) - 2*sys.maxsize == mpq(1 - 4*sys.maxsize, 2)
        assert mpq(1, 2) - 3*sys.maxsize == mpq(1 - 6*sys.maxsize, 2)
        assert mpq(1, 2) - mpz(2) == mpq(-3, 2)

    def test_rsub(self):
        assert mpq(1, 3) - mpq(1, 2) == mpq(-1, 6)
        assert 2 - mpq(1, 2) == mpq(3, 2)
        assert sys.maxsize - mpq(1, 2) == mpq(2*sys.maxsize -1, 2)
        assert 2*sys.maxsize - mpq(1, 2) == mpq(4*sys.maxsize - 1, 2)
        assert 3*sys.maxsize - mpq(1, 2) == mpq(6*sys.maxsize - 1, 2)
        assert mpz(2) - mpq(1, 2) == mpq(3, 2)

    def test_mul(self):
        assert mpq(1, 2) * mpq(1, 3) == mpq(1, 6)
        assert mpq(1, 2) * 2 == mpq(1, 1)
        assert mpq(1, 2) * sys.maxsize == mpq(sys.maxsize, 2)
        assert mpq(1, 2) * (2*sys.maxsize) == mpq(sys.maxsize, 1)
        assert mpq(1, 2) * (3*sys.maxsize) == mpq(3*sys.maxsize, 2)
        assert mpq(1, 2) * (4*sys.maxsize) == mpq(2*sys.maxsize, 1)
        assert mpq(1, 2) * mpz(2) == mpq(1, 1)

    def test_rmul(self):
        assert mpq(1, 3) * mpq(1, 2) == mpq(1, 6)
        assert 2 * mpq(1,2) == mpq(1,1)
        assert sys.maxsize * mpq(1,2) == mpq(sys.maxsize, 2)
        assert (2*sys.maxsize) * mpq(1, 2) == mpq(sys.maxsize, 1)
        assert (3*sys.maxsize) * mpq(1, 2) == mpq(3*sys.maxsize, 2)
        assert (4*sys.maxsize) * mpq(1, 2) == mpq(2*sys.maxsize, 1)
        assert mpz(2) * mpq(1, 2) == mpq(1, 1)

    def test_div(self):
        assert mpq(1, 2) / mpq(1, 3) == mpq(3, 2)
        assert mpq(1, 2) / 2 == mpq(1, 4)
        assert mpq(1, 2) / -2 == mpq(-1, 4)
        assert mpq(1, 2) / sys.maxsize == mpq(1, 2*sys.maxsize)
        assert mpq(1, 2) / (2 * sys.maxsize) == mpq(1, 4 * sys.maxsize)
        assert mpq(1, 2) / (3 * sys.maxsize) == mpq(1, 6 * sys.maxsize)
        assert mpq(1, 2) / (4 * sys.maxsize) == mpq(1, 8 * sys.maxsize)
        assert mpq(1, 2) / mpz(3) == mpq(1, 6)

    def test_zerodiv(self):
        with pytest.raises(ZeroDivisionError):
            mpq(1, 2) // mpq(0, 1)
        with pytest.raises(ZeroDivisionError):
            mpq(1, 2) // mpz(0)
        with pytest.raises(ZeroDivisionError):
            mpq(1, 2) // 0
        with pytest.raises(ZeroDivisionError):
            mpq(1, 2) // 0L

    def test_rdiv(self):
        assert mpq(1, 3) / mpq(1, 2) == mpq(2, 3)
        assert 2 / mpq(3,2) == mpq(4,3)
        assert sys.maxsize / mpq(1,2) == mpq(2*sys.maxsize, 1)
        assert (2*sys.maxsize) / mpq(2, 1) == mpq(sys.maxsize, 1)
        assert (3*sys.maxsize) / mpq(2, 1) == mpq(3*sys.maxsize, 2)
        assert (4*sys.maxsize) / mpq(2, 1) == mpq(2*sys.maxsize, 1)
        assert mpz(3) / mpq(1, 2) == mpq(6, 1)

    def test_zerordiv(self):
        with pytest.raises(ZeroDivisionError):
            1 // mpq(0, 1)
        with pytest.raises(ZeroDivisionError):
            mpz(1) // mpq(0, 1)

    def test_pow(self):
        assert mpq(2,3) ** 3 == mpq(2,3) ** mpz(3) == mpq(8,27)
        assert mpq(-2,3) ** 2 == mpq(-2,3) ** mpz(2) == mpq(4,9)
        assert mpq(-2,3) ** 3 == mpq(-2,3) ** mpz(3) == mpq(-8,27)
        assert mpq(2,3) ** 0 == mpq(2,3) ** mpz(0) == mpq(0,1) ** 0 == mpq(1,1)

        # XXX These Run out of memory - gmp: overflow in mpz type
        # with pytest.raises(OverflowError):
        #      mpq(2, 3) ** (2*sys.maxint + 1)
        # with pytest.raises(OverflowError):
        #      mpq(2, 3) ** -(2*sys.maxint + 1)

    def test_pow_neg_exp(self):
        assert mpq(2,3) ** -3 == mpq(27,8)
        assert mpq(-2,3) ** -2 == mpq(9,4)
        assert mpq(-2,3) ** -3 == mpq(-27,8)

        with pytest.raises(ZeroDivisionError):
            mpq(0,1) ** -3

    def test_pow_mod(self):
        with pytest.raises(TypeError):
            pow(mpq(2,1), 2, 2)

    def test_pow_big_exp(self):
        with pytest.raises(ValueError):
            mpq(2,3) ** (2 * sys.maxint + 2)
        with pytest.raises(ValueError):
            mpq(2,3) ** -(2 * sys.maxint + 2)

    def test_int(self):
        assert int(mpq(1, 2)) == mpq(0, 1)
        assert int(mpq(3, 2)) == mpq(1, 1)
        assert int(mpq(-3, 2)) == mpq(-1, 1)

    def test_long(self):
        assert long(mpq(1, 2)) == mpq(0, 1)
        assert long(mpq(3, 2)) == mpq(1, 1)
        assert long(mpq(-3, 2)) == mpq(-1, 1)

    def test_abs(self):
        assert abs(mpq(1, 2)) == mpq(1, 2)
        assert abs(mpq(-1, 2)) == mpq(1, 2)

    def test_pos(self):
        assert +mpq(1, 2) == mpq(1, 2)
        assert +mpq(-1, 2) == mpq(-1, 2)

    def test_neg(self):
        assert -mpq(1, 2) == mpq(-1, 2)
        assert -mpq(-1, 2) == mpq(1, 2)

    def test_float(self):
        assert float(mpq(1, 2)) == 0.5
        assert float(mpq(-1, 2)) == -0.5

    def test_complex(self):
        assert complex(mpq(1, 2)) == 0.5 + 0j
        assert complex(mpq(-1, 2)) == -0.5 + 0j

    def test_nonzero(self):
        assert bool(mpq(1,2))
        assert bool(mpq(-1,2))
        assert not bool(mpq(0,1))

    def test_floor(self):
        assert mpq(1,2).__floor__() == mpz(0)
        assert mpq(-1,2).__floor__() == mpz(-1)

    def test_ceil(self):
        assert mpq(1,2).__ceil__() == mpz(1)
        assert mpq(-1,2).__ceil__() == mpz(0)

    @pytest.mark.parametrize('n', invalids)
    def test_invalid_type_math(self, n):
        with pytest.raises(TypeError):
            mpq(1, 2) + n
        with pytest.raises(TypeError):
            mpq(1, 2) - n
        with pytest.raises(TypeError):
            n - mpq(1, 2)
        with pytest.raises(TypeError):
            mpq(1, 2) * n
        with pytest.raises(TypeError):
            mpq(1, 2) // n
        with pytest.raises(TypeError):
            n // mpq(1, 2)
        with pytest.raises(TypeError):
            mpq(1, 2) ** n
        with pytest.raises(TypeError):
            n ** mpq(1, 2)


class TestFormat(object):
    def test_str(self):
        assert str(mpq(1, 2)) == "1/2"
        assert str(mpq(-1, 2)) == "-1/2"
        assert str(mpq(2, 1)) == "2"
        assert str(mpq(-2, 1)) == "-2"

    def test_repr(self):
        assert repr(mpq(1, 2)) == "mpq(1,2)"
        assert repr(mpq(-1, 2)) == "mpq(-1,2)"
        assert repr(mpq(2, 1)) == "mpq(2,1)"
        assert repr(mpq(-2, 1)) == "mpq(-2,1)"


class TestCmp(object):
    def test_cmp_mpq(self):
        assert mpq(1,2) > mpq(1,3)
        assert mpq(1,3) < mpq(1,2)
        assert mpq(1,2) == mpq(1,2)
        assert mpq(1,2) >= mpq(1,3)
        assert mpq(1,3) <= mpq(1,2)
        assert mpq(1,2) != mpq(1,3)

    def test_cmp_mpz(self):
        assert mpq(3,2) > mpz(1)
        assert mpq(1,2) < mpz(1)
        assert mpq(2,1) == mpz(2)

    def test_cmp_float(self):
        assert mpq(3,2) > 1.3
        assert mpq(1,2) < 0.6
        assert mpq(1,2) == 0.5
        assert mpq(3,2) == 1.5

    def test_cmp_int(self):
        assert mpq(3,2) > 1
        assert mpq(1,2) < 1
        assert mpq(2,1) == 2

        assert mpq(2*sys.maxsize + 1, 2) > sys.maxsize
        assert mpq(2*sys.maxsize - 1, 2) < sys.maxsize
        assert mpq(sys.maxsize, 1) == sys.maxsize

        assert mpq(4*sys.maxsize + 1, 2) > 2*sys.maxsize
        assert mpq(4*sys.maxsize - 1, 2) < 2*sys.maxsize
        assert mpq(2*sys.maxsize, 1) == 2*sys.maxsize

        assert mpq(6*sys.maxsize + 1, 2) > 3*sys.maxsize
        assert mpq(6*sys.maxsize - 1, 2) < 3*sys.maxsize
        assert mpq(3*sys.maxsize, 1) == 3*sys.maxsize

    def test_hash(self):
        import fractions
        assert hash(mpq(1,2)) == hash(fractions.Fraction(1,2)) == hash(0.5)
        assert hash(mpq(3,2)) == hash(fractions.Fraction(3,2)) == hash(1.5)
        assert hash(mpq(3,1)) == hash(fractions.Fraction(3,1)) == 3
        assert hash(mpq(0)) == hash(fractions.Fraction(0,1)) == hash(0.0) == 0
        assert (hash(mpq(sys.maxsize + 1, sys.maxsize)) ==
                hash(fractions.Fraction(sys.maxsize + 1, sys.maxsize)))

    @pytest.mark.xfail(sys.version_info < (3,), reason="python2 comparison")
    @pytest.mark.parametrize('n', invalids)
    def test_invalid_type_math(self, n):
        with pytest.raises(TypeError):
            mpq(1, 2) > n
        with pytest.raises(TypeError):
            mpq(1, 2) < n
        with pytest.raises(TypeError):
            mpq(1, 2) == n
        with pytest.raises(TypeError):
            mpq(1, 2) != n


class TestMod(object):
    def test_mod(self):
        assert mpq(5, 2) % mpq(1, 3) == mpq(1, 6)
        assert mpq(5, 2) % 2 == mpq(1, 2)
        assert mpq(5, 2) % mpz(2) == mpq(1, 2)

    def test_rmod(self):
        assert 2 % mpq(5, 2) == mpq(2, 1)
        assert mpq(1, 3) % mpq(5, 2) == mpq(1, 3)
        assert mpz(2) % mpq(5, 2) == mpq(2, 1)

    def test_divmod(self):
        assert mpq(5, 2) % -2 == mpq(-3, 2)
        assert divmod(mpq(5, 2), mpq(1,2)) == (mpz(5), mpq(0,1))
        assert divmod(mpq(5, 2), mpz(2)) == (mpz(1), mpq(1,2))
        assert divmod(mpq(5, 2), 2) == (mpz(1), mpq(1,2))
        assert divmod(mpq(5, 2), 2) == (mpz(1), mpq(1,2))
        assert divmod(mpz(2), mpq(3, 4)) == (mpz(2), mpq(1,2))


class TestNumDen(object):
    @pytest.mark.parametrize('n', [-2, -1, 0, 1, 2])
    def test_num(self, n):
        assert mpq(n, 3).numerator == mpz(n)

    @pytest.mark.parametrize('n', [-2, -1, 1, 2])
    def test_den(self, n):
        assert mpq(3, n).denominator == mpz(abs(n))
