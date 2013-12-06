import sys
import pytest


from gmpy_cffi import (
    log, log2, log10, exp, exp2, exp10, cos, sin, tan, sin_cos, sec, csc, cot,
    acos, asin, atan, atan2, cosh, sinh, tanh, sinh_cosh, sech, csch, coth,
    acosh, asinh, atanh, factorial, log1p, expm1, eint, li2, gamma, lngamma,
    lgamma, digamma, zeta, erf, erfc, j0, j1, jn, y0, y1, yn, fma, fms, agm,
    hypot, ai, const_log2, const_pi, const_euler, const_catalan, mpfr, mpq, mpz)


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


class TestSpecial(object):

    def test_factorial(self):
        assert factorial(10**3) == mpfr('4.0238726007709379e+2567')
        with pytest.raises(ValueError):
            factorial(-3)
        with pytest.raises(TypeError):
            factorial(0.5)

    def test_log1p(self):
        assert log1p(1.4) == mpfr('0.87546873735389985')

    def test_expm1(self):
        assert expm1(2.4) == mpfr('10.023176380641601')

    def test_eint(self):
        assert eint(0.5) == mpfr('0.4542199048631736')

    def test_li2(self):
        assert li2(0.5) == mpfr('0.58224052646501245')

    def test_gamma(self):
        assert gamma(0.5) == mpfr('1.7724538509055161')

    def test_lngamma(self):
        assert lngamma(0.5) == mpfr('0.57236494292470008')

    def test_lgamma(self):
        assert lgamma(0.5) == (mpfr('0.57236494292470008'), 1)
        assert lgamma(-0.0) == (mpfr('inf'), -1)

    def test_digamma(self):
        assert digamma(0.5) == mpfr('-1.9635100260214235')

    def test_zeta(self):
        assert zeta(0.5) == mpfr('-1.4603545088095868')

    def test_erf(self):
        assert erf(0.5) == mpfr('0.52049987781304652')

    def test_erfc(self):
        assert erfc(0.5) == mpfr('0.47950012218695348')

    def test_j0(self):
        assert j0(0.5) == mpfr('0.93846980724081286')

    def test_j1(self):
        assert j1(0.5) == mpfr('0.2422684576748739')

    def test_jn(self):
        assert jn(0.5, 4) == mpfr('0.00016073647636428759')
        with pytest.raises(TypeError):
            jn(0.5, sys.maxsize+1)
        with pytest.raises(TypeError):
            jn(0.5, -sys.maxsize-2)

    def test_y0(self):
        assert y0(0.5) == mpfr('-0.44451873350670656')

    def test_y1(self):
        assert y1(0.5) == mpfr('-1.4714723926702431')

    def test_yn(self):
        assert yn(0.5, 4) == mpfr('-499.27256081951231')
        with pytest.raises(TypeError):
            yn(0.5, sys.maxsize+1)
        with pytest.raises(TypeError):
            yn(0.5, -sys.maxsize-2)

    def test_fma(self):
        assert fma(0.5, 0.7, 1.1) == mpfr('1.4500000000000002')

    def test_fms(self):
        assert fms(0.5, 0.7, 1.1) == mpfr('-0.75000000000000011')
        assert fms(0.5, mpfr(0.7), 1.1) == mpfr('-0.75000000000000011')
        assert fms(0.5, 0.7, mpfr(1.1)) == mpfr('-0.75000000000000011')

    def test_agm(self):
        assert agm(0.5, 0.4) == mpfr('0.44860571605752053')

    def test_hypot(self):
        assert hypot(0.5, 0.4) == mpfr('0.6403124237432849')

    def test_ai(self):
        assert ai(0.5) == mpfr('0.23169360648083348')


class TestConst(object):
    def test_const_log2(self):
        assert const_log2() == mpfr('0.69314718055994529')
        assert const_log2(100) == mpfr('0.69314718055994530941723212145798', 100)

    def test_const_pi(self):
        assert const_pi() == mpfr('3.1415926535897931')
        assert const_pi(100) == mpfr('3.1415926535897932384626433832793', 100)

    def test_const_euler(self):
        assert const_euler() == mpfr('0.57721566490153287')
        assert const_euler(100) == mpfr('0.57721566490153286060651209008234', 100)

    def test_const_catalan(self):
        assert const_catalan() == mpfr('0.91596559417721901')
        assert const_catalan(100) == mpfr('0.91596559417721901505460351493252', 100)
