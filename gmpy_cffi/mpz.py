import logging
import sys
import cffi
import array
from types import NoneType

__all__ = "ffi", "gmp", "mpz"

ffi = cffi.FFI()

ffi.cdef("""
    typedef struct { ...; } __mpz_struct;
    typedef __mpz_struct *mpz_t;
    typedef unsigned long mp_bitcnt_t;

    void mpz_init (mpz_t x);
    void mpz_clear (mpz_t x);

    void mpz_set_ui (mpz_t rop, unsigned long int op);
    void mpz_set_si (mpz_t rop, signed long int op);
    void mpz_set_d (mpz_t rop, double op);
    int mpz_set_str (mpz_t rop, char *str, int base);

    unsigned long int mpz_get_ui (mpz_t op);
    signed long int mpz_get_si (mpz_t op);
    double mpz_get_d (mpz_t op);
    char * mpz_get_str (char *str, int base, mpz_t op);
    void mpz_import (mpz_t rop, size_t count, int order, size_t size, int endian, size_t nails, const void *op);
    void * mpz_export (void *rop, size_t *countp, int order, size_t size, int endian, size_t nails, mpz_t op);

    void mpz_add (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_add_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_sub (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_sub_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_ui_sub (mpz_t rop, unsigned long int op1, mpz_t op2);
    void mpz_mul (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_mul_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_submul (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_mul_2exp (mpz_t rop, mpz_t op1, mp_bitcnt_t op2);
    void mpz_neg (mpz_t rop, mpz_t op);
    void mpz_abs (mpz_t rop, mpz_t op);

    void mpz_fdiv_q (mpz_t q, mpz_t n, mpz_t d);
    void mpz_fdiv_q_ui (mpz_t q, mpz_t n, unsigned long int d);
    void mpz_fdiv_r (mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_r_ui (mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_qr (mpz_t q, mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_qr_ui (mpz_t q, mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_q_2exp (mpz_t q, mpz_t n, mp_bitcnt_t b);
//    int mpz_divisible_ui_p (mpz_t n, unsigned long int d);

    void mpz_powm (mpz_t rop, mpz_t base, mpz_t exp, mpz_t mod);
    void mpz_powm_ui (mpz_t rop, mpz_t base, unsigned long int exp, mpz_t mod);
    void mpz_pow_ui (mpz_t rop, mpz_t base, unsigned long int exp);
    void mpz_ui_pow_ui (mpz_t rop, unsigned long int base, unsigned long int exp);

    int mpz_cmp (mpz_t op1, mpz_t op2);
    int mpz_cmp_ui (mpz_t op1, unsigned long int op2);
    int mpz_sgn (mpz_t op);

    void mpz_and (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_ior (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_xor (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_com (mpz_t rop, mpz_t op);

    int mpz_fits_ulong_p (mpz_t op);
    int mpz_fits_slong_p (mpz_t op);
    size_t mpz_sizeinbase (mpz_t op, int base);

//    void mpz_bin_ui (mpz_t rop, mpz_t n, unsigned long int k);
//    void mpz_bin_uiui (mpz_t rop, unsigned long int n, unsigned long int k);
""")

gmp = ffi.verify("#include <gmp.h>", libraries=['gmp', 'm'])

# ____________________________________________________________

MAX_UI = 2 * sys.maxint + 1
#logging.basicConfig(filename='_gmpy.log', level=logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

cache_size = _incache = 100
_cache = []


def _init_cache():
    for _ in xrange(cache_size):
        mpz = ffi.new("mpz_t")
        gmp.mpz_init(mpz)
        _cache.append(mpz)
_init_cache()


def _new_mpz():
    """Return an initialized mpz_t."""
    global _incache

    if _incache:
#        logging.debug('_from_cache: %d', _incache)
        _incache -= 1
        return _cache[_incache]
    else:
#        logging.debug('_new_mpz')
        mpz = ffi.new("mpz_t")
        gmp.mpz_init(mpz)
        return mpz


def _del_mpz(mpz):
    global _incache

    if _incache < cache_size:
#        logging.debug('_to_cache: %d', _incache)
        _cache[_incache] = mpz
        _incache += 1
    else:
#        logging.debug('_del_mpz')
        gmp.mpz_clear(mpz)


def _pylong_to_mpz(n, a):
    """
    Set `a` from `n`.

    :type n: long
    :type a: mpz_t
    """

    neg = n < 0
    n = abs(n)
    #tmp = ffi.new("uint64_t[]", (n.bit_length() + 63) // 64)
    #count = len(tmp)
    #for i in range(count):
    #    n, v = divmod(n, 1 << 64)
    #    tmp[i] = v
    #gmp.mpz_import(a, count, -1, 8, 0, 0, tmp)
    tmp = array.array('L')
    divisor = 1 << (8 * tmp.itemsize)
    while n:
        n, v = divmod(n, divisor)
        tmp.append(v)
    addr, count = tmp.buffer_info()
    gmp.mpz_import(a, count, -1, tmp.itemsize, 0, 0, ffi.cast('void *', addr))
    if neg:
        gmp.mpz_neg(a, a)


def _mpz_to_pylong(a):
    """
    Convert a to a python long.

    :type a: mpz_t
    :rtype: long
    """

    size = ffi.sizeof('uint64_t')
    numb = 8 * size
    count = (gmp.mpz_sizeinbase(a, 2) + numb - 1) // numb
    factor = 1 << numb
    p = ffi.new('uint64_t[]', count)
    gmp.mpz_export(p, ffi.NULL, 1, size, 0, 0, a)
    res = 0
    for n in p:
        res = factor * res + n

    return res * gmp.mpz_sgn(a)


def _mpz_to_str(a, base):
    """
    Return string representation of a in base base.

    :type a: mpz_t
    :param base: 2..62
    :type base: int
    :rtype: str
    """

    l = gmp.mpz_sizeinbase(a, base) + 2
    p = ffi.new('char[]', l)
    gmp.mpz_get_str(p, base, a)
    return ffi.string(p)


class mpz(object):
    _mpz_str = None

    def __init__(self, n, base=None):
        """
        Create a mpz from `n`.

        :param n: Value to convert. Can be an int, a float, a mpz or a string; if float, it gets truncated.
        :type n: int or float or str or mpz
        :param base: Base in which to interpret the string `n`. Only allowed if `n` is a string. If not given, `base` defaults to 10.
        :type base: int or None.
        """

        if isinstance(n, self.__class__):
            self._mpz = n._mpz
            return
        a = self._mpz = ffi.gc(_new_mpz(), _del_mpz)
        if isinstance(n, str):
            if base is None:
                base = 10
            if base == 0 or 2 <= base <= 62:
                if gmp.mpz_set_str(a, n, base) == -1:
                    raise ValueError("Can't create mpz from %s with base %s" % (n, base))
            else:
                raise ValueError('base must be 0 or 2..62, not %s' % base)
        elif base is not None:
            raise ValueError('Base only allowed for str, not for %s.' % type(n))
        elif isinstance(n, float):
            gmp.mpz_set_d(a, n)
        elif -sys.maxint - 1 <= n <= sys.maxint:
            gmp.mpz_set_si(a, n)
        elif sys.maxint < n <= MAX_UI:
            gmp.mpz_set_ui(a, n)
        else:
            assert isinstance(n, long)
            _pylong_to_mpz(n, a)

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
        res = _new_mpz()
        if isinstance(other, (int, long)) and 0 <= other <= MAX_UI:
            gmp.mpz_add_ui(res, self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_add(res, self._mpz, oth)
                _del_mpz(oth)
            else:
                gmp.mpz_add(res, self._mpz, other._mpz)
        return mpz._from_c_mpz(res)
    __radd__ = __add__

    def __sub__(self, other):
        res = _new_mpz()
        if isinstance(other, (int, long)) and 0 <= other <= MAX_UI:
            gmp.mpz_sub_ui(res, self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_sub(res, self._mpz, oth)
                _del_mpz(oth)
            else:
                gmp.mpz_sub(res, self._mpz, other._mpz)
        return mpz._from_c_mpz(res)

    def __rsub__(self, other):
        res = _new_mpz()
        if 0 <= other <= MAX_UI:
            gmp.mpz_ui_sub(res, other, self._mpz)
        elif -MAX_UI <= other < 0:
            gmp.mpz_add_ui(res, self._mpz, -other)
            gmp.mpz_neg(res, res)
        else:
            oth = _new_mpz()
            _pylong_to_mpz(other, oth)
            gmp.mpz_sub(res, oth, self._mpz)
            _del_mpz(oth)
        return mpz._from_c_mpz(res)

    def __mul__(self, other):
        res = _new_mpz()
        if isinstance(other, (int, long)) and 0 <= other <= MAX_UI:
            gmp.mpz_mul_ui(res, self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_mul(res, self._mpz, oth)
                _del_mpz(oth)
            else:
                gmp.mpz_mul(res, self._mpz, other._mpz)
        return mpz._from_c_mpz(res)
    __rmul__ = __mul__

    def __floordiv__(self, other):
        if other == 0:
            raise ZeroDivisionError('mpz division by zero')
        q = _new_mpz()
        if isinstance(other, (int, long)) and 0 < other <= MAX_UI:
            gmp.mpz_fdiv_q_ui(q, self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_fdiv_q(q, self._mpz, oth)
                _del_mpz(oth)
            else:
                gmp.mpz_fdiv_q(q, self._mpz, other._mpz)
        return mpz._from_c_mpz(q)

    def __rfloordiv__(self, other):
        if self == 0:
            raise ZeroDivisionError('mpz division by zero')
        q = _new_mpz()
        oth = _new_mpz()
        _pylong_to_mpz(other, oth)
        gmp.mpz_fdiv_q(q, oth, self._mpz)
        _del_mpz(oth)
        return mpz._from_c_mpz(q)

    __div__ = __floordiv__
    __rdiv__ = __rfloordiv__

    def __mod__(self, other):
        if other == 0:
            raise ZeroDivisionError('mpz modulo by zero')
        r = _new_mpz()
        if isinstance(other, (int, long)) and 0 <= other <= MAX_UI:
            gmp.mpz_fdiv_r_ui(r, self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_fdiv_r(r, self._mpz, oth)
                _del_mpz(oth)
            else:
                gmp.mpz_fdiv_r(r, self._mpz, other._mpz)
        return mpz._from_c_mpz(r)

    def __rmod__(self, other):
        if self == 0:
            raise ZeroDivisionError('mpz modulo by zero')
        r = _new_mpz()
        oth = _new_mpz()
        _pylong_to_mpz(other, oth)
        gmp.mpz_fdiv_r(r, oth, self._mpz)
        _del_mpz(oth)
        return mpz._from_c_mpz(r)

    def __divmod__(self, other):
        if other == 0:
            raise ZeroDivisionError('mpz modulo by zero')
        q = _new_mpz()
        r = _new_mpz()
        if isinstance(other, (int, long)) and 0 <= other <= MAX_UI:
            gmp.mpz_fdiv_qr_ui(q, r, self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                gmp.mpz_fdiv_qr(q, r, self._mpz, oth)
                _del_mpz(oth)
            else:
                gmp.mpz_fdiv_qr(q, r, self._mpz, other._mpz)
        return mpz._from_c_mpz(q), mpz._from_c_mpz(r)

    def __rdivmod__(self, other):
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

    def __cmp__(self, other):
        if isinstance(other, (int, long)) and 0 <= other <= MAX_UI:
            return gmp.mpz_cmp_ui(self._mpz, other)
        else:
            if isinstance(other, (int, long)):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
                res = gmp.mpz_cmp(self._mpz, oth)
                _del_mpz(oth)
            else:
                res = gmp.mpz_cmp(self._mpz, other._mpz)
            return res

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
            if 0 <= other <= MAX_UI:
                gmp.mpz_set_ui(oth, other)
            else:
                _pylong_to_mpz(other, oth)
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
            if 0 <= other <= MAX_UI:
                gmp.mpz_set_ui(oth, other)
            else:
                _pylong_to_mpz(other, oth)
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
            if 0 <= other <= MAX_UI:
                gmp.mpz_set_ui(oth, other)
            else:
                _pylong_to_mpz(other, oth)
            gmp.mpz_xor(res, self._mpz, oth)
            _del_mpz(oth)
        else:
            gmp.mpz_xor(res, self._mpz, other._mpz)

        return mpz._from_c_mpz(res)
    __rxor__ = __xor__

    def __nonzero__(self):
        return gmp.mpz_cmp_ui(self._mpz, 0) != 0

    def __pow__(self, power, modulo=None):
        if not isinstance(power, (int, long, mpz)):
            return NotImplemented
        if not isinstance(modulo, (int, long, mpz, NoneType)):
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
