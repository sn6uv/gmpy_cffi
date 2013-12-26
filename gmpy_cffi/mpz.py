import logging
import sys

from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.convert import _pyint_to_mpz, _pylong_to_mpz, _mpz_to_pylong, _mpz_to_str, MAX_UI
from gmpy_cffi.cache import _new_mpz, _del_mpz


if sys.version > '3':
    long = int
    xrange = range


class mpz(object):
    _mpz_str = None

    def __init__(self, n=0, base=None):
        """
        mpz() -> mpz(0)

            If no argument is given, return mpz(0).

        mpz(n) -> mpz

            Return an 'mpz' object with a numeric value 'n' (truncating n
            to its integer part if it's a Fraction, 'mpq', Decimal, float
            or 'mpfr').

        mpz(s[, base=0]):

            Return an 'mpz' object from a string 's' made of digits in the
            given base.  If base=0, binary, octal, or hex Python strings
            are recognized by leading 0b, 0o, or 0x characters, otherwise
            the string is assumed to be decimal. Values for base can range
            between 2 and 62.
        """

        if isinstance(n, self.__class__):
            self._mpz = n._mpz
            return
        a = self._mpz = ffi.gc(_new_mpz(), _del_mpz)
        if isinstance(n, str):
            if base is None:
                base = 10
            if base == 0 or 2 <= base <= 62:
                if gmp.mpz_set_str(a, n.encode('UTF-8'), base) != 0:
                    raise ValueError("Can't create mpz from %s with base %s" % (n, base))
            else:
                raise ValueError('base must be 0 or 2..62, not %s' % base)
        elif base is not None:
            raise ValueError('Base only allowed for str, not for %s.' % type(n))
        elif isinstance(n, float):
            gmp.mpz_set_d(a, n)
        elif isinstance(n, (int, long)):
            _pyint_to_mpz(n, a)
        else:
            raise TypeError

    @classmethod
    def _from_c_mpz(cls, mpz):
        inst = object.__new__(cls)
        inst._mpz = ffi.gc(mpz, _del_mpz)
        return inst

    def __str__(self):
        if self._mpz_str is None:
            self._mpz_str = _mpz_to_str(self._mpz, 10)
        return self._mpz_str

    def __repr__(self):
        return 'mpz(%s)' % self

    def __hex__(self):
        tmp = '0x' + _mpz_to_str(abs(self)._mpz, 16)
        return tmp if self >= 0 else '-' + tmp

    def __oct__(self):
        tmp = '0' + _mpz_to_str(abs(self)._mpz, 8)
        return tmp if self >= 0 else '-' + tmp

    def __add__(self, other):
        if isinstance(other, (int, long)):
            res = _new_mpz()
            if 0 <= other <= MAX_UI:
                gmp.mpz_add_ui(res, self._mpz, other)
            else:
                _pyint_to_mpz(other, res)
                gmp.mpz_add(res, self._mpz, res)
            return mpz._from_c_mpz(res)
        elif isinstance(other, mpz):
            res = _new_mpz()
            gmp.mpz_add(res, self._mpz, other._mpz)
            return mpz._from_c_mpz(res)
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, (int, long)):
            res = _new_mpz()
            if 0 <= other <= MAX_UI:
                gmp.mpz_sub_ui(res, self._mpz, other)
            else:
                _pylong_to_mpz(other, res)
                gmp.mpz_sub(res, self._mpz, res)
            return mpz._from_c_mpz(res)
        elif isinstance(other, mpz):
            res = _new_mpz()
            gmp.mpz_sub(res, self._mpz, other._mpz)
            return mpz._from_c_mpz(res)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, long)):
            res = _new_mpz()
            if 0 <= other <= MAX_UI:
                gmp.mpz_ui_sub(res, other, self._mpz)
            else:
                _pylong_to_mpz(other, res)
                gmp.mpz_sub(res, res, self._mpz)
            return mpz._from_c_mpz(res)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, long)):
            res = _new_mpz()
            if 0 <= other <= MAX_UI:
                gmp.mpz_mul_ui(res, self._mpz, other)
            else:
                _pylong_to_mpz(other, res)
                gmp.mpz_mul(res, res, self._mpz)
            return mpz._from_c_mpz(res)
        elif isinstance(other, mpz):
            res = _new_mpz()
            gmp.mpz_mul(res, self._mpz, other._mpz)
            return mpz._from_c_mpz(res)
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __floordiv__(self, other):
        if isinstance(other, (int, long)):
            if other == 0:
                raise ZeroDivisionError('mpz division by zero')
            res = _new_mpz()
            if 0 < other <= MAX_UI:
                gmp.mpz_fdiv_q_ui(res, self._mpz, other)
            else:
                _pylong_to_mpz(other, res)
                gmp.mpz_fdiv_q(res, self._mpz, res)
            return mpz._from_c_mpz(res)
        elif isinstance(other, mpz):
            if other == 0:
                raise ZeroDivisionError('mpz division by zero')
            res = _new_mpz()
            gmp.mpz_fdiv_q(res, self._mpz, other._mpz)
            return mpz._from_c_mpz(res)
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, (int, long)):
            if self == 0:
                raise ZeroDivisionError('mpz division by zero')
            res = _new_mpz()
            _pylong_to_mpz(other, res)
            gmp.mpz_fdiv_q(res, res, self._mpz)
            return mpz._from_c_mpz(res)
        else:
            return NotImplemented

    __div__ = __floordiv__
    __rdiv__ = __rfloordiv__

    def __mod__(self, other):
        if isinstance(other, (int, long)):
            if other == 0:
                raise ZeroDivisionError('mpz modulo by zero')
            r = _new_mpz()
            if 0 <= other <= MAX_UI:
                gmp.mpz_fdiv_r_ui(r, self._mpz, other)
            else:
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_fdiv_r(r, self._mpz, oth)
                _del_mpz(oth)
            return mpz._from_c_mpz(r)
        elif isinstance(other, mpz):
            if other == 0:
                raise ZeroDivisionError('mpz modulo by zero')
            r = _new_mpz()
            gmp.mpz_fdiv_r(r, self._mpz, other._mpz)
            return mpz._from_c_mpz(r)
        else:
            return NotImplemented

    def __rmod__(self, other):
        if not isinstance(other, (int, long)):
            return NotImplemented
        if self == 0:
            raise ZeroDivisionError('mpz modulo by zero')
        r = _new_mpz()
        oth = _new_mpz()
        _pylong_to_mpz(other, oth)
        gmp.mpz_fdiv_r(r, oth, self._mpz)
        _del_mpz(oth)
        return mpz._from_c_mpz(r)

    def __divmod__(self, other):
        if isinstance(other, (int, long)):
            if other == 0:
                raise ZeroDivisionError('mpz modulo by zero')
            q = _new_mpz()
            r = _new_mpz()
            if 0 <= other <= MAX_UI:
                gmp.mpz_fdiv_qr_ui(q, r, self._mpz, other)
            else:
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_fdiv_qr(q, r, self._mpz, oth)
                _del_mpz(oth)
            return mpz._from_c_mpz(q), mpz._from_c_mpz(r)
        elif isinstance(other, mpz):
            if other == 0:
                raise ZeroDivisionError('mpz modulo by zero')
            q = _new_mpz()
            r = _new_mpz()
            gmp.mpz_fdiv_qr(q, r, self._mpz, other._mpz)
            return mpz._from_c_mpz(q), mpz._from_c_mpz(r)
        else:
            return NotImplemented

    def __rdivmod__(self, other):
        if not isinstance(other, (int, long)):
            return NotImplemented
        if self == 0:
            raise ZeroDivisionError('mpz modulo by zero')
        q = _new_mpz()
        r = _new_mpz()
        oth = _new_mpz()
        _pylong_to_mpz(other, oth)
        gmp.mpz_fdiv_qr(q, r, oth, self._mpz)
        _del_mpz(oth)
        return mpz._from_c_mpz(q), mpz._from_c_mpz(r)

    def __lshift__(self, other):
        if not isinstance(other, (int, long, mpz)):
            return NotImplemented
        oth = gmp.mpz_get_ui(other._mpz) if isinstance(other, mpz) else other
        res = _new_mpz()
        gmp.mpz_mul_2exp(res, self._mpz, oth)
        return mpz._from_c_mpz(res)

    def __rlshift__(self, other):
        if not isinstance(other, (int, long)):
            return NotImplemented
        return mpz(other) << self

    def __rshift__(self, other):
        if not isinstance(other, (int, long, mpz)):
            return NotImplemented
        oth = gmp.mpz_get_ui(other._mpz) if isinstance(other, mpz) else other
        res = _new_mpz()
        gmp.mpz_fdiv_q_2exp(res, self._mpz, oth)
        return mpz._from_c_mpz(res)

    def __rrshift__(self, other):
        if not isinstance(other, (int, long)):
            return NotImplemented
        return mpz(other) >> self

    def __hash__(self):
        # WTF When this returns -1, CPython silently changes it to -2
        i = int(self)
        if -sys.maxsize - 1 <= i <= sys.maxsize:
            return i
        return (i + sys.maxsize + 1) % (2 * sys.maxsize + 2) - sys.maxsize - 1

    def __cmp(self, other):
        if isinstance(other, mpz):
            res = gmp.mpz_cmp(self._mpz, other._mpz)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                res = gmp.mpz_cmp_ui(self._mpz, other)
            else:
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                res = gmp.mpz_cmp(self._mpz, oth)
                _del_mpz(oth)
        elif isinstance(other, float):
            res = gmp.mpz_cmp_d(self._mpz, other)
        else:
            return None
        return res

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

    def __int__(self):
        if gmp.mpz_fits_slong_p(self._mpz):
            return gmp.mpz_get_si(self._mpz)
        elif gmp.mpz_fits_ulong_p(self._mpz):
            return gmp.mpz_get_ui(self._mpz)
        else:
            return _mpz_to_pylong(self._mpz)

    __index__ = __int__

    def __long__(self):
        if gmp.mpz_fits_slong_p(self._mpz):
            return long(gmp.mpz_get_si(self._mpz))
        elif gmp.mpz_fits_ulong_p(self._mpz):
            return gmp.mpz_get_ui(self._mpz)
        else:
            return _mpz_to_pylong(self._mpz)

    def __float__(self):
        return gmp.mpz_get_d(self._mpz)

    def __complex__(self):
        return float(self) + 0j

    def __abs__(self):
        res = _new_mpz()
        gmp.mpz_abs(res, self._mpz)
        return mpz._from_c_mpz(res)

    def __neg__(self):
        res = _new_mpz()
        gmp.mpz_neg(res, self._mpz)
        return mpz._from_c_mpz(res)

    def __pos__(self):
        return self

    def __invert__(self):
        res = _new_mpz()
        gmp.mpz_com(res, self._mpz)
        return mpz._from_c_mpz(res)

    def __and__(self, other):
        res = _new_mpz()
        if isinstance(other, (int, long)):
            oth = _new_mpz()
            _pyint_to_mpz(other, oth)
            gmp.mpz_and(res, self._mpz, oth)
            _del_mpz(oth)
        else:
            gmp.mpz_and(res, self._mpz, other._mpz)

        return mpz._from_c_mpz(res)
    __rand__ = __and__

    def __or__(self, other):
        res = _new_mpz()
        if isinstance(other, (int, long)):
            oth = _new_mpz()
            _pyint_to_mpz(other, oth)
            gmp.mpz_ior(res, self._mpz, oth)
            _del_mpz(oth)
        else:
            gmp.mpz_ior(res, self._mpz, other._mpz)

        return mpz._from_c_mpz(res)
    __ror__ = __or__

    def __xor__(self, other):
        res = _new_mpz()
        if isinstance(other, (int, long)):
            oth = _new_mpz()
            _pyint_to_mpz(other, oth)
            gmp.mpz_xor(res, self._mpz, oth)
            _del_mpz(oth)
        else:
            gmp.mpz_xor(res, self._mpz, other._mpz)

        return mpz._from_c_mpz(res)
    __rxor__ = __xor__

    def __nonzero__(self):
        return gmp.mpz_cmp_ui(self._mpz, 0) != 0

    __bool__ = __nonzero__

    def __pow__(self, power, modulo=None):
        if not isinstance(power, (int, long, mpz)):
            return NotImplemented
        if modulo is not None and not isinstance(modulo, (int, long, mpz)):
            return NotImplemented

        if power < 0:
            raise ValueError('mpz.pow with negative exponent')

        res = _new_mpz()
        if modulo is None:
            exp = int(power)
            if exp > MAX_UI:
                raise ValueError('mpz.pow with outragous exponent')
            gmp.mpz_pow_ui(res, self._mpz, exp)
        else:
            del_mod = del_exp = False
            if isinstance(modulo, (int, long)):
                mod = _new_mpz()
                _pylong_to_mpz(abs(modulo), mod)
                del_mod = True
            else:
                mod = modulo._mpz
            if isinstance(power, (int, long)) and power <= MAX_UI:
                gmp.mpz_powm_ui(res, self._mpz, power, mod)
            else:
                if isinstance(power, (int, long)):
                    exp = _new_mpz()
                    _pylong_to_mpz(power, exp)
                    del_exp = True
                else:
                    exp = power._mpz
                gmp.mpz_powm(res, self._mpz, exp, mod)
                if del_exp:
                    _del_mpz(exp)
                if del_mod:
                    _del_mpz(mod)

        return mpz._from_c_mpz(res)

    def __rpow__(self, other):
        if not isinstance(other, (int, long)):
            return NotImplemented

        if self < 0:
            raise ValueError('mpz.pow with negative exponent')

        res = _new_mpz()

        exp = int(self)
        if exp > MAX_UI:
            raise ValueError('mpz.pow with outragous exponent')
        if 0 <= other <= MAX_UI:
            gmp.mpz_ui_pow_ui(res, other, exp)
        else:
            base = _new_mpz()
            _pylong_to_mpz(other, base)
            gmp.mpz_pow_ui(res, base, exp)
            _del_mpz(base)

        return mpz._from_c_mpz(res)
