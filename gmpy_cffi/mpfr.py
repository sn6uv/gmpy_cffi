import sys
import math

from gmpy_cffi.mpz import mpz
from gmpy_cffi.mpq import mpq
from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.convert import _mpfr_to_str, _str_to_mpfr, _pyint_to_mpfr, _pylong_to_mpz, MAX_UI, _mpz_to_pylong
from gmpy_cffi.cache import _new_mpfr, _del_mpfr, _new_mpz, _del_mpz


if sys.version > '3':
    long = int
    xrange = range


def isinf(x):
    """
    isinf(x) -> boolean

    Return True if x is +Infinity or -Infinity.
    """
    if isinstance(x, mpfr):
        return bool(gmp.mpfr_inf_p(x._mpfr))
    elif isinstance(x, float):
        return math.isinf(x)
    elif isinstance(x, (int, long, mpz, mpq)):
        return False
    else:
        raise TypeError('isinf() argument type not supported')


def isnan(x):
    """
    isnan(x) -> boolean

    Return True if x is NaN (Not-A-Number).
    """
    if isinstance(x, mpfr):
        return bool(gmp.mpfr_nan_p(x._mpfr))
    elif isinstance(x, float):
        return math.is_nan(x)
    elif isinstance(x, (int, long, mpz, mpq)):
        return False
    else:
        raise TypeError('isinf() argument type not supported')


class mpfr(object):
    _mpfr_str = _repr_str = None
    """
    mpfr() -> mpfr(0.0)

         If no argument is given, return mpfr(0.0).

    mpfr(n[, precison=0]) -> mpfr

         Return an 'mpfr' object after converting a numeric value. If
         no precision, or a precision of 0, is specified; the precison
         is taken from the current context.

    mpfr(s[, precision=0[, [base=0]]) -> mpfr

         Return 'mpfr' object after converting a string 's' made up of
         digits in the given base, possibly with fraction-part (with
         period as a separator) and/or exponent-part (with exponent
         marker 'e' for base<=10, else '@'). If no precision, or a
         precision of 0, is specified; the precison is taken from the
         current context. The base of the string representation must
         be 0 or in the interval 2 ... 62. If the base is 0, the leading
         digits of the string are used to identify the base: 0b implies
         base=2, 0x implies base=16, otherwise base=10 is assumed.
    """
    def __init__(self, *args):
        nargs = len(args)
        if nargs == 1 and isinstance(args[0], self.__class__):
            self._mpfr = args[0]._mpfr
            return

        if nargs > 3:
            raise TypeError("mpfr() requires 0 to 3 arguments")

        if nargs >= 2:
            a = self._mpfr = ffi.gc(_new_mpfr(prec=args[1]), _del_mpfr)
        else:
            a = self._mpfr = ffi.gc(_new_mpfr(), _del_mpfr)

        if nargs == 0:
            gmp.mpfr_set_zero(a, 1)
        elif nargs == 3:
            if isinstance(args[0], str):
                _str_to_mpfr(args[0], args[2], a)
            else:
                raise TypeError('function takes at most 2 arguments (%i given)' % nargs)
        else:
            if isinstance(args[0], str):
                _str_to_mpfr(args[0], 10, a)
            elif isinstance(args[0], float):
                gmp.mpfr_set_d(a, args[0], gmp.MPFR_RNDN)
            elif isinstance(args[0], (int, long)):
                _pyint_to_mpfr(args[0], a)
            elif isinstance(args[0], mpz):
                gmp.mpfr_set_z(a, args[0]._mpz, gmp.MPFR_RNDN)
            elif isinstance(args[0], mpq):
                gmp.mpfr_set_q(a, args[0]._mpq, gmp.MPFR_RNDN)
            else:
                raise TypeError('cannot construct mpfr from %s.' % args[0])

    def __str__(self):
        if self._mpfr_str is None:
            self._mpfr_str = _mpfr_to_str(self._mpfr)
        return self._mpfr_str

    def __repr__(self):
        if self._repr_str is None:
            if self.precision == gmp.mpfr_get_default_prec():
                self._repr_str = "mpfr('%s')" % self
            else:
                self._repr_str = "mpfr('%s',%s)" % (self, self.precision)
        return self._repr_str

    @property
    def precision(self):
        return gmp.mpfr_get_prec(self._mpfr)

    @classmethod
    def _from_c_mpfr(cls, mpfr):
        inst = object.__new__(cls)
        inst._mpfr = ffi.gc(mpfr, _del_mpfr)
        return inst

    def __cmp(self, other):
        if isinstance(other, mpfr):
            return gmp.mpfr_cmp(self._mpfr, other._mpfr)
        elif isinstance(other, float):
            return gmp.mpfr_cmp_d(self._mpfr, other)
        if isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other < sys.maxsize:
                return gmp.mpfr_cmp_ui(self._mpfr, other)
            elif 0 <= other <= MAX_UI:
                return gmp.mpfr_cmp_ui(self._mpfr, other)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                result = gmp.mpfr_cmp_z(self._mpfr, tmp_mpz)
                _del_mpz(tmp_mpz)
                return result
        elif isinstance(other, mpz):
            return gmp.mpfr_cmp_z(self._mpfr, other._mpz)
        elif isinstance(other, mpq):
            return gmp.mpfr_cmp_q(self._mpfr, other._mpq)
        return None

    def __lt__(self, other):
        c = self.__cmp(other)
        if c is None:
            return NotImplemented
        return c < 0

    def __gt__(self, other):
        c = self.__cmp(other)
        if c is None:
            return NotImplemented
        return c > 0

    def __eq__(self, other):
        c = self.__cmp(other)
        if c is None:
            return NotImplemented
        return c == 0

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def __hash__(self):
        # XXX Optimize (see gmpy / how floats are hashed within python)
        return hash(float(self))

    def __add__(self, other):
        res = _new_mpfr()
        if isinstance(other, mpfr):
            gmp.mpfr_add(res, self._mpfr, other._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, mpq):
            gmp.mpfr_add_q(res, self._mpfr, other._mpq, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_add_z(res, self._mpfr, other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_add_d(res, self._mpfr, other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_add_si(res, self._mpfr, other, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_add_ui(res, self._mpfr, other, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_add_z(res, self._mpfr, tmp_mpz, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    __radd__ = __add__

    def __sub__(self, other):
        res = _new_mpfr()
        if isinstance(other, mpfr):
            gmp.mpfr_sub(res, self._mpfr, other._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, mpq):
            gmp.mpfr_sub_q(res, self._mpfr, other._mpq, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_sub_z(res, self._mpfr, other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_sub_d(res, self._mpfr, other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_sub_si(res, self._mpfr, other, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_sub_ui(res, self._mpfr, other, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_sub_z(res, self._mpfr, tmp_mpz, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    def __rsub__(self, other):
        res = _new_mpfr()
        if isinstance(other, mpq):
            # There is no mpfr_q_sub
            gmp.mpfr_sub_q(res, self._mpfr, other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_neg(res, res, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_z_sub(res, other._mpz, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_d_sub(res, other, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_si_sub(res, other, self._mpfr, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_ui_sub(res, other, self._mpfr, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_z_sub(res, tmp_mpz, self._mpfr, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    def __mul__(self, other):
        res = _new_mpfr()
        if isinstance(other, mpfr):
            gmp.mpfr_mul(res, self._mpfr, other._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, mpq):
            gmp.mpfr_mul_q(res, self._mpfr, other._mpq, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_mul_z(res, self._mpfr, other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_mul_d(res, self._mpfr, other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_mul_si(res, self._mpfr, other, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_mul_ui(res, self._mpfr, other, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_mul_z(res, self._mpfr, tmp_mpz, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        res = _new_mpfr()
        if isinstance(other, mpfr):
            gmp.mpfr_div(res, self._mpfr, other._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, mpq):
            gmp.mpfr_div_q(res, self._mpfr, other._mpq, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_div_z(res, self._mpfr, other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_div_d(res, self._mpfr, other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_div_si(res, self._mpfr, other, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_div_ui(res, self._mpfr, other, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_div_z(res, self._mpfr, tmp_mpz, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        if self == 0:
            raise ZeroDivisionError
        res = _new_mpfr()
        if isinstance(other, mpq):
            # There is no mpfr_q_div
            gmp.mpfr_set_q(res, other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_div(res, res, self._mpfr, gmp.MPFR_RNDN)
            pass
        elif isinstance(other, mpz):
            # There is no mpfr_z_div
            gmp.mpfr_set_z(res, other._mpz, gmp.MPFR_RNDN)
            gmp.mpfr_div(res, res, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_d_div(res, other, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_si_div(res, other, self._mpfr, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_ui_div(res, other, self._mpfr, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_set_z(res, tmp_mpz, gmp.MPFR_RNDN)
                gmp.mpfr_div(res, res, self._mpfr, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    def __pow__(self, other):
        res = _new_mpfr()
        if isinstance(other, mpfr):
            gmp.mpfr_pow(res, self._mpfr, other._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, mpq):
            # There is no mpfr_pow_q
            gmp.mpfr_set_q(res, other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_pow(res, self._mpfr, res, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_pow_z(res, self._mpfr, other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            # There is no mpfr_pow_d
            gmp.mpfr_set_d(res, other, gmp.MPFR_RNDN)
            gmp.mpfr_pow(res, self._mpfr, res, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpfr_pow_si(res, self._mpfr, other, gmp.MPFR_RNDN)
            elif 0 <= other <= MAX_UI:
                gmp.mpfr_pow_ui(res, self._mpfr, other, gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pylong_to_mpz(other, tmp_mpz)
                gmp.mpfr_pow_z(res, self._mpfr, tmp_mpz, gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    def __rpow__(self, other):
        res = _new_mpfr()
        if isinstance(other, mpq):
            # There is no mpfr_pow_q
            gmp.mpfr_set_q(res, other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_pow(res, res, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            # There is no mpfr_pow_z
            gmp.mpfr_set_z(res, other._mpz, gmp.MPFR_RNDN)
            gmp.mpfr_pow(res, res, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            # There is no mpfr_pow_d
            gmp.mpfr_set_d(res, other, gmp.MPFR_RNDN)
            gmp.mpfr_pow(res, res, self._mpfr, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            # There is no mpfr_si_pow
            _pyint_to_mpfr(other, res)
            gmp.mpfr_pow(res, res, self._mpfr, gmp.MPFR_RNDN)
        else:
            return NotImplemented
        return mpfr._from_c_mpfr(res)

    def __pos__(self):
        return self

    def __neg__(self):
        res = _new_mpfr()
        gmp.mpfr_neg(res, self._mpfr, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)

    def __abs__(self):
        res = _new_mpfr()
        gmp.mpfr_abs(res, self._mpfr, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)

    def __trunc__(self):
        tmp_mpfr = _new_mpfr()
        gmp.mpfr_trunc(tmp_mpfr, self._mpfr)
        res = gmp.mpfr_get_d(tmp_mpfr, gmp.MPFR_RNDN)
        _del_mpfr(tmp_mpfr)
        return res

    def __float__(self):
        return gmp.mpfr_get_d(self._mpfr, gmp.MPFR_RNDN)

    def __int__(self):
        if not gmp.mpfr_number_p(self._mpfr):
            raise ValueError("Cannot convert '%s' to int" % self)
        elif gmp.mpfr_fits_slong_p(self._mpfr, gmp.MPFR_RNDN):
            return gmp.mpfr_get_si(self._mpfr, gmp.MPFR_RNDN)
        elif gmp.mpfr_fits_ulong_p(self._mpfr, gmp.MPFR_RNDN):
            return gmp.mpfr_get_ui(self._mpfr, gmp.MPFR_RNDN)
        else:
            tmp_mpz = _new_mpz()
            gmp.mpfr_get_z(tmp_mpz, self._mpfr, gmp.MPFR_RNDN)
            res = _mpz_to_pylong(tmp_mpz)
            _del_mpz(tmp_mpz)
            return res

    __long__ = __int__
