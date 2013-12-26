import sys
import logging

import gmpy_cffi
from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.convert import _mpq_to_str, _str_to_mpq, _pyint_to_mpz, _pyint_to_mpq, MAX_UI
from gmpy_cffi.mpz import mpz
from gmpy_cffi.cache import _new_mpq, _del_mpq, _new_mpz, _del_mpz


if sys.version > '3':
    long = int
    xrange = range


class mpq(object):
    _mpq_str = _numerator = _denominator = None

    def __init__(self, *args):
        """
        mpq() -> mpq(0,1)

             If no argument is given, return mpq(0,1).

        mpq(n) -> mpq

             Return an 'mpq' object with a numeric value n. Decimal and
             Fraction values are converted exactly.

        mpq(n,m) -> mpq

             Return an 'mpq' object with a numeric value n/m.

        mpq(s[, base=10]) -> mpq

             Return an 'mpq' object from a string s made up of digits in
             the given base. s may be made up of two numbers in the same
             base separated by a '/' character.
        """

        #TODO kwargs (base)

        nargs = len(args)
        if nargs == 1 and isinstance(args[0], self.__class__):
            self._mpq = args[0]._mpq
            return

        a = self._mpq = ffi.gc(_new_mpq(), _del_mpq)

        if nargs == 0:
            gmp.mpq_set_ui(a, 0, 1)
        elif nargs == 1:
            if isinstance(args[0], float):
                gmp.mpq_set_d(a, args[0])
            elif isinstance(args[0], (int, long)):
                _pyint_to_mpq(args[0], a)
            elif isinstance(args[0], mpz):
                gmp.mpq_set_z(a, args[0]._mpz)
            elif isinstance(args[0], str):
                _str_to_mpq(args[0], 10, a)
            else:
                raise TypeError('mpq() requires numeric or string argument')
        elif nargs == 2:
            if isinstance(args[0], str):
                _str_to_mpq(args[0], args[1], a)
            elif all(isinstance(arg, (int, long, mpz)) for arg in args):
                # Set Numerator
                if isinstance(args[0], mpz):
                    gmp.mpq_set_num(a, args[0]._mpz)
                else:
                    num = gmp.mpq_numref(a)
                    _pyint_to_mpz(args[0], num)

                # Set Denominator
                if args[1] == 0:
                    raise ZeroDivisionError("zero denominator in 'mpq'")

                if isinstance(args[1], mpz):
                    gmp.mpq_set_den(a, args[1]._mpz)
                else:
                    den = gmp.mpq_denref(a)
                    _pyint_to_mpz(args[1], den)
            else:
                # Numerator
                if isinstance(args[0], mpq):
                    gmp.mpq_set(a, args[0]._mpq)
                elif isinstance(args[0], float):
                    gmp.mpq_set_d(a, args[0])
                elif isinstance(args[0], (int, long)):
                    _pyint_to_mpq(args[0], a)
                elif isinstance(args[0], mpz):
                    gmp.mpq_set_z(a, args[0]._mpz)
                else:
                    raise TypeError('mpq() requires numeric or string argument')

                # Denominator
                b = _new_mpq()
                if isinstance(args[1], mpq):
                    gmp.mpq_set(b, args[1]._mpq)
                elif isinstance(args[1], float):
                    gmp.mpq_set_d(b, args[1])
                elif isinstance(args[1], (int, long)):
                    _pyint_to_mpq(args[1], b)
                elif isinstance(args[1], mpz):
                    gmp.mpq_set_z(b, args[1]._mpz)
                else:
                    raise TypeError('mpq() requires numeric or string argument')

                # Divide them
                if gmp.mpq_sgn(b) == 0:
                    _del_mpq(b)
                    raise ZeroDivisionError

                gmp.mpq_div(a, a, b)
                _del_mpq(b)
        else:
            raise TypeError("mpq() requires 0, 1 or 2 arguments")

        # TODO only canonicalize when required (e.g. optimize mpq(42))
        gmp.mpq_canonicalize(a)

    @property
    def numerator(self):
        if self._numerator is None:
            num = _new_mpz()
            gmp.mpq_get_num(num, self._mpq)
            self._numerator = mpz._from_c_mpz(num)
        return self._numerator

    @property
    def denominator(self):
        if self._denominator is None:
            den = _new_mpz()
            gmp.mpq_get_den(den, self._mpq)
            self._denominator = mpz._from_c_mpz(den)
        return self._denominator

    @classmethod
    def _from_c_mpq(cls, mpq):
        inst = object.__new__(cls)
        inst._mpq = ffi.gc(mpq, _del_mpq)
        return inst

    def __str__(self):
        if self._mpq_str is None:
            self._mpq_str = _mpq_to_str(self._mpq, 10)
        return self._mpq_str

    def __repr__(self):
        tmp = ("%s" % self).split('/')
        if len(tmp) == 1:
            tmp.append('1')
        return "mpq(%s,%s)" % tuple(tmp)

    def __add__(self, other):
        if isinstance(other, mpq):
            res = _new_mpq()
            gmp.mpq_add(res, self._mpq, other._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, (int, long)):
            res = _new_mpq()
            _pyint_to_mpq(other, res)
            gmp.mpq_add(res, self._mpq, res)
            return mpq._from_c_mpq(res)
        elif isinstance(other, mpz):
            res = _new_mpq()
            gmp.mpq_set_z(res, other._mpz)
            gmp.mpq_add(res, self._mpq, res)
            return mpq._from_c_mpq(res)
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, mpq):
            res = _new_mpq()
            gmp.mpq_sub(res, self._mpq, other._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, (int, long)):
            res = _new_mpq()
            _pyint_to_mpq(other, res)
            gmp.mpq_sub(res, self._mpq, res)
            return mpq._from_c_mpq(res)
        elif isinstance(other, mpz):
            res = _new_mpq()
            gmp.mpq_set_z(res, other._mpz)
            gmp.mpq_sub(res, self._mpq, res)
            return mpq._from_c_mpq(res)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, long)):
            res = _new_mpq()
            _pyint_to_mpq(other, res)
            gmp.mpq_sub(res, res, self._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, mpz):
            res = _new_mpq()
            gmp.mpq_set_z(res, other._mpz)
            gmp.mpq_sub(res, res, self._mpq)
            return mpq._from_c_mpq(res)
        else:
            return NotImplemented

    def __mul__(self, other):
        res = _new_mpq()
        if isinstance(other, mpq):
            gmp.mpq_mul(res, self._mpq, other._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, (int, long)):
            res = _new_mpq()
            _pyint_to_mpq(other, res)
            gmp.mpq_mul(res, res, self._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, mpz):
            res = _new_mpq()
            gmp.mpq_set_z(res, other._mpz)
            gmp.mpq_mul(res, res, self._mpq)
            return mpq._from_c_mpq(res)
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __floordiv__(self, other):
        if isinstance(other, mpq):
            if gmp.mpq_sgn(other._mpq) == 0:
                raise ZeroDivisionError
            res = _new_mpq()
            gmp.mpq_div(res, self._mpq, other._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, (int, long)):
            if other == 0:
                raise ZeroDivisionError
            res = _new_mpq()
            _pyint_to_mpq(other, res)
            gmp.mpq_div(res, self._mpq, res)
            return mpq._from_c_mpq(res)
        elif isinstance(other, mpz):
            if gmp.mpz_sgn(other._mpz) == 0:
                raise ZeroDivisionError
            res = _new_mpq()
            gmp.mpq_set_z(res, other._mpz)
            gmp.mpq_div(res, self._mpq, res)
            return mpq._from_c_mpq(res)
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, (int, long)):
            if gmp.mpq_sgn(self._mpq) == 0:
                raise ZeroDivisionError
            res = _new_mpq()
            _pyint_to_mpq(other, res)
            gmp.mpq_div(res, res, self._mpq)
            return mpq._from_c_mpq(res)
        elif isinstance(other, mpz):
            if gmp.mpq_sgn(self._mpq) == 0:
                raise ZeroDivisionError
            res = _new_mpq()
            gmp.mpq_set_z(res, other._mpz)
            gmp.mpq_div(res, res, self._mpq)
            return mpq._from_c_mpq(res)
        else:
            return NotImplemented

    __div__ = __floordiv__
    __rdiv__ = __rfloordiv__

    def __truediv__(self, other):
        return NotImplemented

    def __rtruediv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        # XXX Optimize
        return self - (self // other).__floor__() * other

    def __rmod__(self, other):
        # XXX Optimize
        return other - (other // self).__floor__() * self

    def __divmod__(self, other):
        # XXX Optimize
        div = (self // other).__floor__()
        return (div, self - div * other)

    def __rdivmod__(self, other):
        # XXX Optimize
        div = (other // self).__floor__()
        return (div, other - div * self)

    def __hash__(self):
        """
        Agrees with fractions.Fractions
        """
        # XXX since this method is expensive, consider caching the result
        if self == int(self):
            return int(self)
        if self == float(self):
            return hash(float(self))
        else:
            num = long(mpz._from_c_mpz(gmp.mpq_numref(self._mpq)))
            den = long(mpz._from_c_mpz(gmp.mpq_denref(self._mpq))) 
            return hash((num, den))

    def __cmp(self, other):
        if isinstance(other, mpq):
            res = gmp.mpq_cmp(self._mpq, other._mpq)
        elif isinstance(other, mpz):
            tmp_mpq = _new_mpq()
            gmp.mpq_set_z(tmp_mpq, other._mpz)
            res = gmp.mpq_cmp(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        elif isinstance(other, (int, long)):
            tmp_mpq = _new_mpq()
            _pyint_to_mpq(other, tmp_mpq)
            res = gmp.mpq_cmp(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        elif isinstance(other, float):
            tmp_mpq = _new_mpq()
            gmp.mpq_set_d(tmp_mpq, other)
            res = gmp.mpq_cmp(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        else:
            return None
        return res

    def __gt__(self, other):
        c = self.__cmp(other)
        if c is None:
            return NotImplemented
        return c > 0

    def __lt__(self, other):
        c = self.__cmp(other)
        if c is None:
            return NotImplemented
        return c < 0

    def __eq__(self, other):
        if isinstance(other, mpq):
            res = gmp.mpq_equal(self._mpq, other._mpq)
        elif isinstance(other, mpz):
            tmp_mpq = _new_mpq()
            gmp.mpq_set_z(tmp_mpq, other._mpz)
            res = gmp.mpq_equal(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        elif isinstance(other, (int, long)):
            tmp_mpq = _new_mpq()
            _pyint_to_mpq(other, tmp_mpq)
            res = gmp.mpq_equal(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        elif isinstance(other, float):
            tmp_mpq = _new_mpq()
            gmp.mpq_set_d(tmp_mpq, other)
            res = gmp.mpq_equal(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        else:
            return NotImplemented
        return res != 0

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __int__(self):
        res = _new_mpz()
        gmp.mpz_tdiv_q(res, gmp.mpq_numref(self._mpq), gmp.mpq_denref(self._mpq))
        return int(mpz._from_c_mpz(res))

    def __long__(self):
        res = _new_mpz()
        gmp.mpz_tdiv_q(res, gmp.mpq_numref(self._mpq), gmp.mpq_denref(self._mpq))
        return long(mpz._from_c_mpz(res))

    def __float__(self):
        return gmp.mpq_get_d(self._mpq)

    def __abs__(self):
        res = _new_mpq()
        gmp.mpq_abs(res, self._mpq)
        return mpq._from_c_mpq(res)

    def __neg__(self):
        res = _new_mpq()
        gmp.mpq_neg(res, self._mpq)
        return mpq._from_c_mpq(res)

    def __ceil__(self):
        res = _new_mpz()
        gmp.mpz_cdiv_q(res, gmp.mpq_numref(self._mpq), gmp.mpq_denref(self._mpq))
        return mpz._from_c_mpz(res)

    def __floor__(self):
        res = _new_mpz()
        gmp.mpz_fdiv_q(res, gmp.mpq_numref(self._mpq), gmp.mpq_denref(self._mpq))
        return mpz._from_c_mpz(res)

    # def __round__(self, other):
    #     raise NotImplementedError

    def __pos__(self):
        return self

    def __nonzero__(self):
        return gmp.mpq_sgn(self._mpq) != 0

    __bool__ = __nonzero__

    def __pow__(self, other, modulo=None):
        if modulo is not None:
            raise TypeError("mpq.pow() no modulo allowed")

        if isinstance(other, mpq):
            # XXX Optimize
            return self ** gmpy_cffi.mpfr(other)
        elif isinstance(other, (mpz, int, long)):
            other = int(other)
            if 0 <= other <= MAX_UI:
                res = _new_mpq()
                gmp.mpz_pow_ui(
                    gmp.mpq_numref(res), gmp.mpq_numref(self._mpq), other)
                gmp.mpz_pow_ui(
                    gmp.mpq_denref(res), gmp.mpq_denref(self._mpq), other)
                return mpq._from_c_mpq(res)
            elif -MAX_UI <= other < 0:
                if self == 0:
                    raise ZeroDivisionError(
                        "mpq.pow() 0 base to negative exponent")
                res = _new_mpq()
                gmp.mpz_pow_ui(
                    gmp.mpq_numref(res), gmp.mpq_denref(self._mpq), -other)
                gmp.mpz_pow_ui(
                    gmp.mpq_denref(res), gmp.mpq_numref(self._mpq), -other)

                # For Example mpq(-1,1)**-1 == mpq(1, -1) -> mpq(1, 1)
                gmp.mpq_canonicalize(res)
                return mpq._from_c_mpq(res)
            else:
                raise ValueError('mpz.pow with outragous exponent')
        else:
            return NotImplemented

    def __rpow__(self, other, modulo=None):
        if modulo is not None:
            raise TypeError("mpq.pow() no modulo allowed")

        return other ** gmpy_cffi.mpfr(self)
