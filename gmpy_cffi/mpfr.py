import sys

from gmpy_cffi.mpz import mpz, _new_mpz, _del_mpz
from gmpy_cffi.mpq import mpq
from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.convert import _mpfr_to_str, _str_to_mpfr, _pyint_to_mpfr, _pylong_to_mpz

# from gmpy_cffi.convert import _pyint_to_mpz, _pylong_to_mpz, _mpz_to_pylong, _mpz_to_str, MAX_UI

if sys.version > '3':
    long = int
    xrange = range


cache_size = _incache = 100
_cache = []


def _init_cache():
    for _ in xrange(cache_size):
        mpfr = ffi.new("mpfr_t")
        gmp.mpfr_init(mpfr)
        _cache.append(mpfr)
_init_cache()


def _new_mpfr(prec=0):
    """Return an initialized mpfr_t."""
    global _incache

    if isinstance(prec, (int, long)):
        if not (prec == 0 or gmp.MPFR_PREC_MIN <= prec <= gmp.MPFR_PREC_MAX):
            raise ValueError( "invalid prec %i (wanted %s <= prec <= %s)" % (
                    prec, gmp.MPFR_PREC_MIN, gmp.MPFR_PREC_MAX))
    else:
        raise TypeError('an integer is required')

    if _incache:
        _incache -= 1
        # Set default precision
        if prec == 0:
            gmp.mpfr_set_prec(_cache[_incache], gmp.mpfr_get_default_prec())
        else:
            gmp.mpfr_set_prec(_cache[_incache], prec)
        return _cache[_incache]
    else:
        mpfr = ffi.new("mpfr_t")
        if prec == 0:
            gmp.mpfr_init(mpfr)
        else:
            gmp.mpfr_init2(mpfr, prec)
        return mpfr


def _del_mpfr(mpfr):
    global _incache

    if _incache < cache_size:
        _cache[_incache] = mpfr
        _incache += 1
    else:
        gmp.mpfr_clear(mpfr)


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
        if len(args) == 1 and isinstance(args[0], self.__class__):
            self._mpfr = args[0]._mpfr
            return

        if len(args) > 3:
            raise TypeError("mpfr() requires 0 to 3 arguments")

        if len(args) == 2:
            a = self._mpfr = ffi.gc(_new_mpfr(prec=args[1]), _del_mpfr)
        else:
            a = self._mpfr = ffi.gc(_new_mpfr(), _del_mpfr)

        if len(args) == 0:
            gmp.mpfr_set_zero(a, 1)
        elif len(args) == 3:
            if isinstance(args[0], str):
                _str_to_mpfr(args[0], args[2], a)
            else:
                raise TypeError('function takes at most 2 arguments (%i given)' % len(args))
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
                pylong_to_mpz(other, tmp_mpz)
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
