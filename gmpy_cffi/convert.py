import sys
import array
from math import log10

from gmpy_cffi.interface import gmp, ffi


MAX_UI = 2 * sys.maxsize + 1


def _pyint_to_mpz(n, a):
    """
    Set `a` from `n`.
    :type n: int,long
    :type a: mpz_t
    """

    if -sys.maxsize - 1 <= n <= sys.maxsize:
        gmp.mpz_set_si(a, n)
    elif sys.maxsize < n <= MAX_UI:
        gmp.mpz_set_ui(a, n)
    else:
        _pylong_to_mpz(n, a)


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
    size = tmp.itemsize
    numb = (8 * size)
    mask = ~(~0 << numb)
    while n:
        v = n & mask
        n = n >> numb
        tmp.append(v)
    addr, count = tmp.buffer_info()
    gmp.mpz_import(a, count, -1, size, 0, 0, ffi.cast('void *', addr))
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
    p = ffi.new('uint64_t[]', count)
    gmp.mpz_export(p, ffi.NULL, 1, size, 0, 0, a)
    res = 0
    for n in p:
        res = (res << numb) + n

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


def _pyint_to_mpq(n, a):
    if -sys.maxsize - 1 <= n <= sys.maxsize:
        gmp.mpq_set_si(a, n, 1)
    elif sys.maxsize < n <= MAX_UI:
        gmp.mpq_set_ui(a, n, 1)
    else:
        assert isinstance(n, long)
        num, den = gmp.mpq_numref(a), gmp.mpq_denref(a)
        _pylong_to_mpz(n, num)
        gmp.mpz_set_ui(den, 1)


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


def _mpfr_to_str(a):
    precision = int(log10(2) * gmp.mpfr_get_prec(a) + 2)
    buf = ffi.new('char []', precision + 10)
    fmtstr = "%.{0}Rg".format(precision)
    buflen = gmp.mpfr_sprintf(buf, fmtstr, a)
    pybuf = ffi.string(buf)
    if '.' not in pybuf:
        pybuf = pybuf + '.0'
    return "mpfr('%s')" % pybuf
