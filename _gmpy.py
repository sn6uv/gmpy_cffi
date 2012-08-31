import sys
import cffi
import array

__all__ = "ffi", "lib", "mpz"

ffi = cffi.FFI()

ffi.cdef("""
    typedef struct { ...; } __mpz_struct;
    typedef __mpz_struct *mpz_t;

//    void mpz_init (mpz_t x);
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
    void mpz_mul (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_mul_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_submul (mpz_t rop, mpz_t op1, mpz_t op2);
//    void mpz_neg (mpz_t rop, mpz_t op);

    void mpz_fdiv_qr (mpz_t q, mpz_t r, mpz_t n, mpz_t d);
//    int mpz_divisible_ui_p (mpz_t n, unsigned long int d);

    int mpz_cmp (mpz_t op1, mpz_t op2);

//    void mpz_bin_ui (mpz_t rop, mpz_t n, unsigned long int k);
//    void mpz_bin_uiui (mpz_t rop, unsigned long int n, unsigned long int k);
""")

lib = ffi.verify("#include <gmp.h>", libraries=['gmp', 'm'])

# ____________________________________________________________

def _pylong_to_mpz(n, a):
    """
    Set mpz `a` from int `n` > 2 * sys.maxint + 1.
    """

    #tmp = ffi.new("uint64_t[]", (n.bit_length() + 63) // 64)
    #count = len(tmp)
    #for i in range(count):
    #    n, v = divmod(n, 1 << 64)
    #    tmp[i] = v
    #lib.mpz_import(a, count, -1, 8, 0, 0, tmp)
    tmp = array.array('L')
    divisor = 1 << (8 * tmp.itemsize)
    while n:
        n, v = divmod(n, divisor)
        tmp.append(v)
    addr, count = tmp.buffer_info()
    lib.mpz_import(a, count, -1, tmp.itemsize, 0, 0, ffi.cast('void *', addr))

def mpz(n, base=None):
    """
    Create a mpz from `n`.

    `n`: Value to convert. Can be an int, a float or a string; if float, it gets truncated.
    `base`: Base in which to interpret the string `n`. Only allowed if `n` is a string. If not given, `base` defaults to 10.
    """
    a = ffi.new("mpz_t")
    if isinstance(n, str):
        if base is None:
            base = 10
        if base == 0 or 2 <= base <= 62:
            if lib.mpz_init_set_str(a, n, base) == -1:
                lib.mpz_clear(a)
                raise ValueError("Can't create mpz from %s with base %s" % (n, base))
        else:
            raise ValueError('base must be 0 or 2..62, not %s' % base)
    elif base is not None:
        raise ValueError('Base only allowed for str, not for %s.' % type(n))
    elif isinstance(n, float):
        lib.mpz_init_set_d(a, n)
    elif -sys.maxint - 1 <= n <= sys.maxint:
        lib.mpz_init_set_si(a, n)
    elif n <= 2 * sys.maxint + 1:
        lib.mpz_init_set_ui(a, n)
    else:
        neg = n < 0
        _pylong_to_mpz(abs(n), a)
        if neg:
            lib.mpz_neg(a, a)

    return a
