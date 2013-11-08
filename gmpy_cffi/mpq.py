import sys
import logging

from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.mpz import _pylong_to_mpz, mpz, _mpz_to_str, _new_mpz, _del_mpz, MAX_UI


if sys.version > '3':
    long = int
    xrange = range


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


def _str_to_mpq(s, base, a):
    if base == 0 or 2 <= base <= 62:
        if gmp.mpq_set_str(a, s, base) == -1:
            raise ValueError("Can't create mpq from %s with base %s" % (s, base))
    else:
        raise ValueError('base must be 0 or 2..62, not %s' % base)


class mpq(object):
    _mpq_str = None

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

        if len(args) == 1 and isinstance(args[0], self.__class__):
            self._mpq = args[0]._mpq
            return

        a = self._mpq = ffi.gc(_new_mpq(), _del_mpq)

        if len(args) == 0:
            gmp.mpq_set_ui(a, 0, 1)
        elif len(args) == 1:
            if isinstance(args[0], float):
                gmp.mpq_set_d(a, args[0])
            elif isinstance(args[0], (int, long)):
                if -sys.maxsize - 1 <= args[0] <= sys.maxsize:
                    gmp.mpq_set_si(a, args[0], 1)
                elif sys.maxsize < args[0] <= MAX_UI:
                    gmp.mpq_set_ui(a, args[0], 1)
                else:
                    assert isinstance(args[0], long)
                    tmp = gmp.mpq_numref(a)
                    _pylong_to_mpz(args[0], tmp)
            elif isinstance(args[0], mpz):
                gmp.mpq_set_z(a, args[0]._mpz)
            elif isinstance(args[0], str):
                _str_to_mpq(args[0], 10, a)
            else:
                raise TypeError('mpq() requires numeric or string argument')
        elif len(args) == 2:
            if isinstance(args[0], str):
                _str_to_mpq(args[0], args[1], a)
            elif all(isinstance(arg, (int, long, mpz)) for arg in args):
                # Set Numerator
                if isinstance(args[0], mpz):
                    gmp.mpq_set_num(a, args[0]._mpz)
                else:
                    num = gmp.mpq_numref(a)
                    if -sys.maxsize - 1 <= args[0] <= sys.maxsize:
                        gmp.mpz_set_si(num, args[0])
                    elif sys.maxsize < args[0] <= MAX_UI:
                        gmp.mpz_set_ui(num, args[0])
                    else:
                        assert isinstance(args[0], long)
                        _pylong_to_mpz(args[0], num)

                # Set Denominator
                if args[1] == 0:
                    raise ZeroDivisionError("zero denominator in 'mpq'")

                if isinstance(args[1], mpz):
                    gmp.mpq_set_den(a, args[1]._mpz)
                else:
                    den = gmp.mpq_denref(a)
                    if -sys.maxsize - 1 <= args[1] <= sys.maxsize:
                        gmp.mpz_set_si(den, args[1])
                    elif sys.maxsize < args[1] <= MAX_UI:
                        gmp.mpz_set_ui(den, args[1])
                    else:
                        assert isinstance(args[1], long)
                        _pylong_to_mpz(args[1], den)
            else:
                # Numerator
                if isinstance(args[0], mpq):
                    gmp.mpq_set(a, args[0]._mpq)
                elif isinstance(args[0], float):
                    gmp.mpq_set_d(a, args[0])
                elif isinstance(args[0], (int, long)):
                    if -sys.maxsize - 1 <= args[0] <= sys.maxsize:
                        gmp.mpq_set_si(a, args[0], 1)
                    elif sys.maxsize < args[0] <= MAX_UI:
                        gmp.mpq_set_ui(a, args[0], 1)
                    else:
                        assert isinstance(args[0], long)
                        num, den = gmp.mpq_numref(a), gmp.mpq_denref(a)
                        _pylong_to_mpz(args[0], num)
                        gmp.mpz_set_ui(den, 1)
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
                    if -sys.maxsize - 1 <= args[1] <= sys.maxsize:
                        gmp.mpq_set_si(b, args[1], 1)
                    elif sys.maxsize < args[1] <= MAX_UI:
                        gmp.mpq_set_ui(b, args[1], 1)
                    else:
                        assert isinstance(args[1], long)
                        num, den = gmp.mpq_numref(b), gmp.mpq_denref(b)
                        _pylong_to_mpz(args[1], num)
                        gmp.mpz_set_ui(den, 1)
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
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpq_set_si(res, other, 1)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpq_set_ui(res, other, 1)
            else:
                assert isinstance(other, long)
                _pylong_to_mpz(other, gmp.mpq_numref(res))
                gmp.mpz_set_ui(gmp.mpq_denref(res), 1)
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
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpq_set_si(res, other, 1)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpq_set_ui(res, other, 1)
            else:
                assert isinstance(other, long)
                _pylong_to_mpz(other, gmp.mpq_numref(res))
                gmp.mpz_set_ui(gmp.mpq_denref(res), 1)
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
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpq_set_si(res, other, 1)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpq_set_ui(res, other, 1)
            else:
                assert isinstance(other, long)
                _pylong_to_mpz(other, gmp.mpq_numref(res))
                gmp.mpz_set_ui(gmp.mpq_denref(res), 1)
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
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpq_set_si(res, other, 1)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpq_set_ui(res, other, 1)
            else:
                assert isinstance(other, long)
                _pylong_to_mpz(other, gmp.mpq_numref(res))
                gmp.mpz_set_ui(gmp.mpq_denref(res), 1)
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
            if -sys.maxsize - 1 <= other < 0:
                gmp.mpq_set_si(res, -1, -other)
            elif 0 < other <= sys.maxsize:
                gmp.mpq_set_si(res, 1, other)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpq_set_ui(res, 1, other)
            else:
                assert isinstance(other, long)
                _pylong_to_mpz(other, gmp.mpq_denref(res))
                gmp.mpz_set_ui(gmp.mpq_numref(res), 1)
            gmp.mpq_mul(res, res, self._mpq)
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
            gmp.mpq_inv(res, self._mpq)
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpz_mul_si(gmp.mpq_numref(res), gmp.mpq_numref(res), other)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpz_mul_ui(gmp.mpq_numref(res), gmp.mpq_numref(res), other)
            else:
                assert isinstance(other, long)
                # Possible optimisation - _pylong_mul_mpz
                _pylong_to_mpz(other, gmp.mpq_numref(res))
                gmp.mpz_mul(gmp.mpq_numref(res),
                            gmp.mpq_numref(res), gmp.mpq_denref(self._mpq))
            gmp.mpq_canonicalize(res)
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
            return hash((
                int(mpz._from_c_mpz(gmp.mpq_numref(self._mpq))),
                int(mpz._from_c_mpz(gmp.mpq_denref(self._mpq)))))

    def __cmp(self, other):
        if isinstance(other, mpq):
            res = gmp.mpq_cmp(self._mpq, other._mpq)
        elif isinstance(other, mpz):
            tmp_mpq = _new_mpq()
            gmp.mpq_set_z(tmp_mpq, other._mpz)
            res = gmp.mpq_cmp(self._mpq, tmp_mpq)
            _del_mpq(tmp_mpq)
        elif isinstance(other, (int, long)):
            tmp_mpz = _new_mpz()
            tmp_mpq = _new_mpq()
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpz_set_si(tmp_mpz, other)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpz_set_ui(tmp_mpz, other)
            else:
                _pylong_to_mpz(other, tmp_mpz)
            gmp.mpq_set_z(tmp_mpq, tmp_mpz)
            res = gmp.mpq_cmp(self._mpq, tmp_mpq)
            _del_mpz(tmp_mpz)
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
            tmp_mpz = _new_mpz()
            tmp_mpq = _new_mpq()
            if -sys.maxsize - 1 <= other <= sys.maxsize:
                gmp.mpz_set_si(tmp_mpz, other)
            elif sys.maxsize < other <= MAX_UI:
                gmp.mpz_set_ui(tmp_mpz, other)
            else:
                _pylong_to_mpz(other, tmp_mpz)
            gmp.mpq_set_z(tmp_mpq, tmp_mpz)
            res = gmp.mpq_equal(self._mpq, tmp_mpq)
            _del_mpz(tmp_mpz)
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

    # def __pow__(self, other, modulo=None):
    #     raise NotImplementedError

    # def __rpow__(self, other):
    #     raise NotImplementedError
