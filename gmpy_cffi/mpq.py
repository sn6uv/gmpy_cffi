import sys
import logging

from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.mpz import _pylong_to_mpz, mpz, _mpz_to_str


cache_size = _incache = 100
_cache = []


def _init_cache():
    for _ in xrange(cache_size):
        mpq = ffi.new("mpq_t")
        gmp.mpq_init(mpq)
        _cache.append(mpq)
_init_cache()


def _new_mpq():
    """Return an initialized mpq_t."""
    global _incache

    if _incache:
#        logging.debug('_from_cache: %d', _incache)
        _incache -= 1
        return _cache[_incache]
    else:
#        logging.debug('_new_mpq')
        mpq = ffi.new("mpq_t")
        gmp.mpq_init(mpq)
        return mpq


def _del_mpq(mpq):
    global _incache

    if _incache < cache_size:
#        logging.debug('_to_cache: %d', _incache)
        _cache[_incache] = mpq
        _incache += 1
    else:
#        logging.debug('_del_mpq')
        gmp.mpq_clear(mpq)


def _mpq_to_str(a, base):
        l = (gmp.mpz_sizeinbase(gmp.mpq_numref(a), base) +
             gmp.mpz_sizeinbase(gmp.mpq_denref(a), base) + 3)
        p = ffi.new('char[]', l)
        gmp.mpq_get_str(ffi.NULL, base, a)
        gmp.mpq_get_str(p, base, a)
        return ffi.string(p)

class mpq(object):
    _mpq_str = None

    def __init__(self, n=0, m=1, base=None):
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

        if isinstance(n, self.__class__):
            self._mpq = n._mpq
            return
        a = self._mpq = ffi.gc(_new_mpq(), _del_mpq)
        if isinstance(n, str):
            if base is None:
                base = 10
            if base == 0 or 2 <= base <= 62:
                if gmp.mpq_set_str(a, n, base) == -1:
                    raise ValueError("Can't create mpq from %s with base %s" % (n, base))
                return
            else:
                raise ValueError('base must be 0 or 2..62, not %s' % base)
        elif base is not None:
            raise ValueError('Base only allowed for str, not for %s.' % type(n))

        assert isinstance(n, (int, long, mpz))
        assert isinstance(m, (int, long, mpz))

        if m == 0:
            raise ZeroDivisionError("zero denominator in 'mpq'")

        # TODO  Optimize this
        gmp.mpq_set_num(a, mpz(n)._mpz)
        gmp.mpq_set_den(a, mpz(m)._mpz)
        gmp.mpq_canonicalize(a)

    def __str__(self):
        if self._mpq_str is None:
            self._mpq_str = _mpq_to_str(self._mpq, 10)
        return self._mpq_str

    def __repr__(self):
        tmp = ("%s" % self).split('/')
        if len(_str) == 1:
            tmp.append('1')
        return "mpq(%s,%s)" % tuple(tmp)
