import pytest


from gmpy_cffi import mpfr, cos, sin, tan, acos, asin, atan, log, log2, log10, exp, exp2, exp10


class TestTrig(object):
    def test_exp(self):
       assert exp(0.5) == exp(mpfr(0.5)) == mpfr('1.6487212707001282')

    def test_exp2(self):
       assert exp2(0.5) == exp2(mpfr(0.5)) == mpfr('1.4142135623730951')

    def test_exp10(self):
       assert exp10(0.5) == exp10(mpfr(0.5)) == mpfr('3.1622776601683795')

    def test_log(self):
       assert log(0.5) == log(mpfr(0.5)) == mpfr('-0.69314718055994529')

    def test_log2(self):
       assert log2(0.5) == log2(mpfr(0.5)) == mpfr('-1.0')

    def test_log10(self):
       assert log10(0.5) == log10(mpfr(0.5)) == mpfr('-0.3010299956639812')

    def test_cos(self):
       assert cos(0.5) == cos(mpfr(0.5)) == mpfr('0.87758256189037276')

    def test_sin(self):
       assert sin(0.5) == sin(mpfr(0.5)) == mpfr('0.47942553860420301')

    def test_tan(self):
       assert tan(0.5) == tan(mpfr(0.5)) == mpfr('0.54630248984379048')

    def test_acos(self):
       assert acos(0.5) == acos(mpfr(0.5)) == mpfr('1.0471975511965979')

    def test_asin(self):
       assert asin(0.5) == asin(mpfr(0.5)) == mpfr('0.52359877559829893')

    def test_atan(self):
       assert atan(0.5) == atan(mpfr(0.5)) == mpfr('0.46364760900080609')
