import sys
import pytest


from gmpy_cffi import (
    log, log2, log10, exp, exp2, exp10, cos, sin, tan, sin_cos, sec, csc, cot,
    acos, asin, atan, atan2, cosh, sinh, tanh, sinh_cosh, sech, csch, coth,
    acosh, asinh, atanh, mpfr, mpq, mpz)


class TestTrig(object):

    def test_init_check(self):
        assert log(mpfr(0.5)) == log(mpq(1, 2)) == mpfr('-0.69314718055994529')
        assert log(2) == log(mpz(2)) == mpfr('0.69314718055994529')
        with pytest.raises(TypeError):
            log([])

    def test_log(self):
        assert log(0.5) == mpfr('-0.69314718055994529')

    def test_log2(self):
        assert log2(0.5) == mpfr('-1.0')

    def test_log10(self):
        assert log10(0.5) == mpfr('-0.3010299956639812')

    def test_exp(self):
        assert exp(0.5) == mpfr('1.6487212707001282')

    def test_exp2(self):
        assert exp2(0.5) == mpfr('1.4142135623730951')

    def test_exp10(self):
        assert exp10(0.5) == mpfr('3.1622776601683795')

    def test_cos(self):
        assert cos(0.5) == mpfr('0.87758256189037276')

    def test_sin(self):
        assert sin(0.5) == mpfr('0.47942553860420301')

    def test_tan(self):
        assert tan(0.5) == mpfr('0.54630248984379048')

    def test_acos(self):
        assert acos(0.5) == mpfr('1.0471975511965979')

    def test_asin(self):
        assert asin(0.5) == mpfr('0.52359877559829893')

    def test_atan(self):
        assert atan(0.5) == mpfr('0.46364760900080609')

    def test_sin_cos(self):
        assert sin_cos(0.5) == sin_cos(mpfr(0.5)) == (sin(0.5), cos(0.5))
        assert sin_cos(0) == (mpfr(0.0), mpfr(1.0))
        assert sin_cos(mpq(1, 3)) == (sin(mpq(1, 3)), cos(mpq(1, 3)))
        assert sin_cos(mpz(3)) == (sin(mpz(3)), cos(mpz(3)))
        with pytest.raises(TypeError):
            sin_cos([])

    def test_sec(self):
        assert sec(0.5) == mpfr('1.139493927324549')

    def test_csc(self):
        assert csc(0.5) == mpfr('2.0858296429334882')

    def test_cot(self):
        assert cot(0.5) == mpfr('1.830487721712452')

    def test_acos(self):
        assert acos(0.5) == mpfr('1.0471975511965979')

    def test_asin(self):
        assert asin(0.5) == mpfr('0.52359877559829893')

    def test_atan(self):
        assert atan(0.5) == mpfr('0.46364760900080609')

    def test_atan2(self):
        assert atan2(1, 2) == atan2(1.0, 2) == atan2(mpfr(1), 2) == mpfr('0.46364760900080609')
        assert atan2(1.5, mpfr(3.1)) == atan2(1.5, 3.1) == mpfr('0.45066132608063364')
        assert atan2(mpq(1, 2), 0.5) == atan2(0.5, mpq(1, 2)) == atan2(0.5, 0.5)
        assert atan2(mpz(3), mpz(2)) == atan2(3, 2) == mpfr('0.98279372324732905')
        with pytest.raises(TypeError):
            atan2(1.4, [])
        with pytest.raises(TypeError):
            atan2([], 1.4)

    def test_sinh(self):
        assert sinh(0.5) == mpfr('0.52109530549374738')

    def test_cosh(self):
        assert cosh(0.5) == mpfr('1.1276259652063807')

    def test_tanh(self):
        assert tanh(0.5) == mpfr('0.46211715726000974')

    def test_sinh_cosh(self):
        assert sinh_cosh(0.5) == sinh_cosh(mpfr(0.5)) == (sinh(0.5), cosh(0.5))
        assert sinh_cosh(0) == (mpfr(0.0), mpfr(1.0))
        assert sinh_cosh(mpq(1, 3)) == (sinh(mpq(1, 3)), cosh(mpq(1, 3)))
        assert sinh_cosh(mpz(3)) == (sinh(mpz(3)), cosh(mpz(3)))
        with pytest.raises(TypeError):
            sinh_cosh([])

    def test_sech(self):
        assert sech(0.5) == mpfr('0.88681888397007391')

    def test_csch(self):
        assert csch(0.5) == mpfr('1.9190347513349437')

    def test_coth(self):
        assert coth(0.5) == mpfr('2.1639534137386529')

    def test_acosh(self):
        assert acosh(1.5) == mpfr('0.96242365011920694')

    def test_asinh(self):
        assert asinh(0.5) == mpfr('0.48121182505960347')

    def test_atanh(self):
        assert atanh(0.5) == mpfr('0.549306144334054846')
