import sys
import cffi
import array

__all__ = "ffi", "gmp", "mpz"

ffi = cffi.FFI()

ffi.cdef("""
    typedef struct { ...; } __mpz_struct;
    typedef __mpz_struct *mpz_t;
    typedef unsigned long mp_bitcnt_t;

    void mpz_init (mpz_t x);
    void mpz_init_set_ui (mpz_t rop, unsigned long int op);
    void mpz_init_set_si (mpz_t rop, signed long int op);
    void mpz_init_set_d (mpz_t rop, double op);
    int mpz_init_set_str (mpz_t rop, char *str, int base);
    void mpz_clear (mpz_t x);

    char * mpz_get_str (char *str, int base, mpz_t op);
    void mpz_import (mpz_t rop, size_t count, int order, size_t size, int endian, size_t nails, const void *op);
//    void * mpz_export (void *rop, size_t *countp, int order, size_t size, int endian, size_t nails, mpz_t op);

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

    void mpz_fdiv_q (mpz_t q, mpz_t n, mpz_t d);
    void mpz_fdiv_q_ui (mpz_t q, mpz_t n, unsigned long int d);
    void mpz_fdiv_r (mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_r_ui (mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_qr (mpz_t q, mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_qr_ui (mpz_t q, mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_q_2exp (mpz_t q, mpz_t n, mp_bitcnt_t b);
//    int mpz_divisible_ui_p (mpz_t n, unsigned long int d);

    int mpz_cmp (mpz_t op1, mpz_t op2);
    int mpz_cmp_ui (mpz_t op1, unsigned long int op2);

//    void mpz_bin_ui (mpz_t rop, mpz_t n, unsigned long int k);
//    void mpz_bin_uiui (mpz_t rop, unsigned long int n, unsigned long int k);
""")

gmp = ffi.verify("#include <gmp.h>", libraries=['gmp', 'm'])

# ____________________________________________________________

MAX_UI = 2 * sys.maxint + 1

def _new_mpz():
    """Return an initialized c mpz."""

    mpz = ffi.new("mpz_t")
    gmp.mpz_init(mpz)
    return mpz

def _pylong_to_mpz(n, a):
    """
    Set mpz `a` from int `n` > 2 * sys.maxint + 1.
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

class mpz(object):
    _mpz_str = None

    def __init__(self, n, base=None):
        """
        Create a mpz from `n`.

        `n`: Value to convert. Can be an int, a float or a string; if float, it gets truncated.
        `base`: Base in which to interpret the string `n`. Only allowed if `n` is a string. If not given, `base` defaults to 10.
        """

        a = self._mpz = ffi.new("mpz_t")
        if isinstance(n, str):
            if base is None:
                base = 10
            if base == 0 or 2 <= base <= 62:
                if gmp.mpz_init_set_str(a, n, base) == -1:
                    gmp.mpz_clear(a)
                    raise ValueError("Can't create mpz from %s with base %s" % (n, base))
            else:
                raise ValueError('base must be 0 or 2..62, not %s' % base)
        elif base is not None:
            raise ValueError('Base only allowed for str, not for %s.' % type(n))
        elif isinstance(n, float):
            gmp.mpz_init_set_d(a, n)
        elif -sys.maxint - 1 <= n <= sys.maxint:
            gmp.mpz_init_set_si(a, n)
        elif n <= MAX_UI:
            gmp.mpz_init_set_ui(a, n)
        else:
            _pylong_to_mpz(n, a)

    @classmethod
    def _from_c_mpz(cls, mpz):
        inst = object.__new__(cls)
        inst._mpz = mpz
        return inst

    def __str__(self):
        if self._mpz_str is None:
            self._mpz_str = ffi.string(gmp.mpz_get_str(ffi.NULL, 10, self._mpz))
        return self._mpz_str

    def __repr__(self):
        return 'mpz(%s)' % self

    def __add__(self, other):
        res = _new_mpz()
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            gmp.mpz_add_ui(res, self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            gmp.mpz_add(res, self._mpz, oth)
        return mpz._from_c_mpz(res)
    __radd__ = __add__

    def __sub__(self, other):
        res = _new_mpz()
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            gmp.mpz_sub_ui(res, self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            gmp.mpz_sub(res, self._mpz, oth)
        return mpz._from_c_mpz(res)

    def __rsub__(self, other):
        res = _new_mpz()
        gmp.mpz_ui_sub(res, other, self._mpz)
        return mpz._from_c_mpz(res)

    def __mul__(self, other):
        res = _new_mpz()
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            gmp.mpz_mul_ui(res, self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            gmp.mpz_mul(res, self._mpz, oth)
        return mpz._from_c_mpz(res)
    __rmul__ = __mul__

    def __div__(self, other):
        q = _new_mpz()
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            gmp.mpz_fdiv_q_ui(q, self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            gmp.mpz_fdiv_q(q, self._mpz, oth)
        return mpz._from_c_mpz(q)

    def __rdiv__(self, other):
        q = _new_mpz()
        gmp.mpz_fdiv_q(q, mpz(other)._mpz, self._mpz)
        return mpz._from_c_mpz(q)

    __floordiv__ = __div__
    __rfloordiv__ = __rdiv__

    def __mod__(self, other):
        r = _new_mpz()
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            gmp.mpz_fdiv_r_ui(r, self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            gmp.mpz_fdiv_r(r, self._mpz, oth)
        return mpz._from_c_mpz(r)

    def __rmod__(self, other):
        r = _new_mpz()
        gmp.mpz_fdiv_r(r, mpz(other)._mpz, self._mpz)
        return mpz._from_c_mpz(r)

    def __divmod__(self, other):
        q = _new_mpz()
        r = _new_mpz()
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            gmp.mpz_fdiv_qr_ui(q, r, self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            gmp.mpz_fdiv_qr(q, r, self._mpz, oth)
        return mpz._from_c_mpz(q), mpz._from_c_mpz(r)

    def __rdivmod__(self, other):
        q = _new_mpz()
        r = _new_mpz()
        gmp.mpz_fdiv_qr(q, r, mpz(other)._mpz, self._mpz)
        return mpz._from_c_mpz(q), mpz._from_c_mpz(r)

    def __lshift__(self, other):
        res = _new_mpz()
        gmp.mpz_mul_2exp(res, self._mpz, other)
        return mpz._from_c_mpz(res)

    def __rshift__(self, other):
        res = _new_mpz()
        gmp.mpz_fdiv_q_2exp(res, self._mpz, other)
        return mpz._from_c_mpz(res)

    def __cmp__(self, other):
        if isinstance(other, int) and 0 <= other <= MAX_UI:
            return gmp.mpz_cmp_ui(self._mpz, other)
        else:
            if isinstance(other, int):
                oth = _new_mpz()
                _pylong_to_mpz(other, oth)
            else:
                oth = other._mpz
            return gmp.mpz_cmp(self._mpz, oth)
